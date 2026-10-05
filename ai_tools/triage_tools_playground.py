from ai_tools.triage import classify_failure

error = 'psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint "users_email_key"\nDETAIL:  Key (email)=(eve@test.com) already exists.'

print(classify_failure(error))