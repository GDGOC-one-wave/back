import os
import json
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AIService:
    @staticmethod
    def verify_phase1(step1_data: Dict, step2_data: Dict) -> Dict:
        """1,2단계 사업성 검증"""
        prompt = f"""당신은 전략적 사업 코치입니다. 다음 데이터를 분석하여 JSON 형식으로 응답하세요.
        데이터: {json.dumps({**step1_data, **step2_data})}
        응답 형식: {{"score": 85, "passed": true, "feedback": "...", "suggestions": ["..."]}}"""
        
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{{"role": "system", "content": prompt}}],
            response_format={{"type": "json_object"}}
        )
        return json.loads(response.choices[0].message.content)

    @staticmethod
    def simulate_bm(all_data: Dict) -> Dict:
        """BM 시뮬레이션 및 수치 산출"""
        prompt = f"""당신은 Venture Builder입니다. 다음 데이터를 바탕으로 BM 시뮬레이션을 수행하고 JSON으로 응답하세요.
        데이터: {json.dumps(all_data)}
        응답 형식: {{"score": 90, "status": "...", "bm": {{...}}, "simulation": {{...}}, "riskFactor": "..."}}"""

        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{{"role": "system", "content": prompt}}],
            response_format={{"type": "json_object"}}
        )
        return json.loads(response.choices[0].message.content)

    @staticmethod
    def get_guided_questions(current_field: str, next_label: str, form_data: Dict) -> List[str]:
        """다음 단계 작성을 위한 유도 질문 생성"""
        prompt = f"""당신은 전략 멘토입니다. [{current_field}] 작성을 마친 사용자에게 다음 항목 [{next_label}] 작성을 위한 날카로운 질문 3가지를 생성하세요.
        현재 데이터: {json.dumps(form_data)}
        반드시 다음 JSON 형식을 따르세요: {{"questions": ["질문1", "질문2", "질문3"]}}"""

        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{{"role": "system", "content": prompt}}],
            response_format={{"type": "json_object"}}
        )
        return json.loads(response.choices[0].message.content).get("questions", [])

    @staticmethod
    def chat_with_mentor(step: int, form_data: Dict, message: str) -> str:
        """멘토와 자유 대화"""
        context = f"현재 단계: {step}, 데이터: {json.dumps(form_data)}"
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {{"role": "system", "content": f"당신은 소크라테스형 멘토입니다. 짧게 조언하세요. 컨텍스트: {context}"}},
                {{"role": "user", "content": message}}
            ]
        )
        return response.choices[0].message.content
