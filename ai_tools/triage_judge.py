from ai_tools.triage import classify_failure_with_reasoning, judge_classification

error = 'psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint "users_email_key"\nDETAIL:  Key (email)=(eve@test.com) already exists.'

answer = classify_failure_with_reasoning(error)
print("Ответ модели:", answer)

verdict = judge_classification(error, answer)
print("Вердикт судьи:", verdict)