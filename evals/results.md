# Evaluation Results

Model: `claude-opus-4-8` &middot; Embeddings: `sentence-transformers/all-MiniLM-L6-v2` &middot; top_k: 5

**Retrieval hit rate:** 100% (12/12 answerable questions)
**Answer faithfulness:** 100% (14/14 questions, includes correct abstentions)

| ID | Question | Answerable | Retrieval Hit | Faithful |
| --- | --- | --- | --- | --- |
| hr-1 | How many vacation days do full-time employees accrue per year? | yes | yes | yes |
| hr-2 | Do unused vacation days roll over into the next year? | yes | yes | yes |
| hr-3 | What is the daily meal reimbursement limit during business travel? | yes | yes | yes |
| security-1 | What is the minimum required password length? | yes | yes | yes |
| security-2 | How often must passwords be rotated? | yes | yes | yes |
| security-3 | Within how long must a suspected security incident be reported? | yes | yes | yes |
| onboarding-1 | How many days do new employees have to enroll in benefits? | yes | yes | yes |
| onboarding-2 | How close to the start date is a new hire's laptop shipped? | yes | yes | yes |
| onboarding-3 | What do engineering new hires need to complete before getting production access? | yes | yes | yes |
| product-1 | How much does the Growth plan cost per month? | yes | yes | yes |
| product-2 | Are monthly plans eligible for refunds? | yes | yes | yes |
| product-3 | What is the first-response SLA for Starter plan customers? | yes | yes | yes |
| unanswerable-1 | What is the company's parental leave policy? | no | - | yes |
| unanswerable-2 | Who is the company's CEO? | no | - | yes |
