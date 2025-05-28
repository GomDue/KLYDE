from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from news.models import Article  # 뉴스 모델 import

def truncate_text(text, max_chars=3000):
    return text[:max_chars] + "..." if len(text) > max_chars else text

def save_history(session, key, messages):
    """세션에 JSON 직렬화 가능한 메시지 저장"""
    session[key] = [
        {"role": "user", "text": m.content} if isinstance(m, HumanMessage)
        else {"role": "bot", "text": m.content}
        for m in messages
    ]

def load_history(session, key):
    """세션에서 메시지를 불러와 LangChain 메시지로 복원"""
    return [
        HumanMessage(content=m["text"]) if m["role"] == "user"
        else AIMessage(content=m["text"])
        for m in session.get(key, [])
    ]


class ChatQAView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        article_id = request.data.get("article_id")
        raw_question = request.data.get("question", "")
        question = raw_question.strip() if isinstance(raw_question, str) else ""

        if not question or not article_id:
            return Response({"message": "Question and article_id are required."}, status=400)

        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return Response({"message": "Article not found."}, status=404)

        chat = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

        # 🔁 세션 기반 히스토리 불러오기 및 추가
        session_key = f"chat_history_{article_id}"
        history = load_history(request.session, session_key)
        history.append(HumanMessage(content=question))

        system_prompt = f"""
        You are Newsie, a multilingual and friendly AI assistant who helps users understand news articles.
        You can answer questions about the article, summarize it, extract keywords, and translate it into Korean if requested.
        You can also understand and respond to questions written in Korean.
        If the question is not about this article at all (e.g., about cooking or movies), then respond with: 
        "Sorry, I couldn't find that information in this article."

        ### Title: {article.title}
        ### Date: {article.write_date.strftime('%Y-%m-%d')}
        ### Content: {truncate_text(article.content)}
        """

        messages = [SystemMessage(content=system_prompt)] + history

        # ✅ 최신 LangChain invoke 방식 사용
        response = chat.invoke(messages)

        # ✅ 응답 저장
        history.append(AIMessage(content=response.content))
        save_history(request.session, session_key, history)

        return Response({
            "message": "Question processed successfully.",
            "response": response.content
        })

