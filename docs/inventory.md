# Collections

## licensing_regulations
Description: Regulations issued under the Khyber Pakhtunkhwa Health Care Commission (KP HCC) Act, 2015, covering healthcare establishment registration, licensing, regulatory authorities, complaints, and related procedures.
Documents: licencing_regulations.pdf
Pages / chunks: (fill in after loading)

## health_policy_kpk
Description: Provincial health policies, strategies, reforms, and programmes of Khyber Pakhtunkhwa, including healthcare governance and the provincial health system following the 18th Constitutional Amendment.
Documents: health_policy_kpk
Pages / chunks: (fill in after loading)

# Embedding
Model: BAAI/bge-base-en-v1.5
Dimension: 768
Chunk size: 800, overlap: 120 (starting values)


---

## Test Questions

### Q1
Question:Who will issue the provisional licence?
Expected collection: licensing_regulations
Expected answer:A Provisional Licence shall be issued by the competent authority to such HCE,
which has submitted an application and its staff is trained on the relevant MSDS
Source (file, page):licencing_regulation,7

### Q2
Question:How will the cancellation of licence occurs?
Expected collection: licensing_regulations
Expected answer:All things like showcase and other letter should first submitted to committe for review and further the committe will decide to cancel the licence in the light of term and conditions
Source (file, page):licensing_regulations,11

(Q3 and Q4: same format, licensing_regulations)

### Q5
Question:
Expected collection: health_policy_kpk
Expected answer:
Source (file, page):

(Q6, Q7, Q8: same format, health_policy_kpk)

### Q9 (needs both)
Question:
Expected collection: both
Expected answer:
Source (file, page):

### Q10 (unanswerable)
Question:
Expected collection: none
Expected answer: I don't know
Source: not in the documents