#Different templates for the generation of the few-shot learning examples

CCNA_5_SHOT_TEMPLATE = """
The following are multiple choice questions (with answers) about network fundamentals, network access,
security fundamentals, automation and programmability. Here are five examples:

Question: Which two options are the best reasons to use an IPV4 private IP space? (Choose two.)
A. to enable intra-enterprise communication
B. to implement NAT
C. to connect applications
D. to conserve global address space
E. to manage routing overhead
Answer: AD

Question: Security Group Access requires which three syslog messages to be sent to Cisco ISE? (Choose three.)
A. IOS-7-PROXY_DROP
B. AP-1-AUTH_PROXY_DOS_ATTACK
C. MKA-2-MACDROP
D. AUTHMGR-5-MACMOVE
E. ASA-6-CONNECT_BUILT
F. AP-1-AUTH_PROXY_FALLBACK_REQ
Answer: BDF

Question: Which two authentication stores are supported to design a wireless network using PEAP EAP-MSCHAPv2 as the authentication method? (Choose two.)
A. Microsoft Active Directory
B. ACS
C. LDAP
D. RSA Secure-ID
E. Certificate Server
Answer: AB

Question: The corporate security policy requires multiple elements to be matched in an authorization policy. Which elements can be combined to meet the requirement?
A. Device registration status and device activation status
B. Network access device and time condition
C. User credentials and server certificate
D. Built-in profile and custom profile
Answer: B

Question: Which three posture states can be used for authorization rules? (Choose three.)
A. unknown
B. known
C. noncompliant
D. quarantined
E. compliant
F. no access
G. limited
Answer: ACE

Question: {Exam_Question}
{Exam_Choices}
Answer: """

CCNA_5_SHOT_TEMPLATE_NO_WHITESPACE_AT_FINAL_ANW = """The following are multiple choice questions (with answers) about network fundamentals, network access,
security fundamentals, automation and programmability.

Question: Which two options are the best reasons to use an IPV4 private IP space? (Choose two.)
A. to enable intra-enterprise communication
B. to implement NAT
C. to connect applications
D. to conserve global address space
E. to manage routing overhead
Answer: AD

Question: Security Group Access requires which three syslog messages to be sent to Cisco ISE? (Choose three.)
A. IOS-7-PROXY_DROP
B. AP-1-AUTH_PROXY_DOS_ATTACK
C. MKA-2-MACDROP
D. AUTHMGR-5-MACMOVE
E. ASA-6-CONNECT_BUILT
F. AP-1-AUTH_PROXY_FALLBACK_REQ
Answer: BDF

Question: Which two authentication stores are supported to design a wireless network using PEAP EAP-MSCHAPv2 as the authentication method? (Choose two.)
A. Microsoft Active Directory
B. ACS
C. LDAP
D. RSA Secure-ID
E. Certificate Server
Answer: AB

Question: The corporate security policy requires multiple elements to be matched in an authorization policy. Which elements can be combined to meet the requirement?
A. Device registration status and device activation status
B. Network access device and time condition
C. User credentials and server certificate
D. Built-in profile and custom profile
Answer: B

Question: Which three posture states can be used for authorization rules? (Choose three.)
A. unknown
B. known
C. noncompliant
D. quarantined
E. compliant
F. no access
G. limited
Answer: ACE

Question: {Exam_Question}
{Exam_Choices}
Answer:"""

FEW_SHOT_TEMPLATE_MMLU = """The following are multiple choice questions (with answers) about computer security.

Question: What is ethical hacking?
A. "Hacking" ethics so they justify unintended selfish behavior
B. Hacking systems (e.g., during penetration testing) to expose vulnerabilities so they can be fixed, rather than exploited
C. Hacking into systems run by those whose ethics you disagree with
D. A slang term for rapid software development, e.g., as part of hackathons
Answer: B

Question: The ____________ is anything which your search engine cannot search.
A. Haunted web
B. World Wide Web
C. Surface web
D. Deep Web
Answer: D

Question: SHA-1 has a message digest of
A. 160 bits
B. 512 bits
C. 628 bits
D. 820 bits
Answer: A

Question: Exploitation of the Heartbleed bug permits
A. overwriting cryptographic keys in memory
B. a kind of code injection
C. a read outside bounds of a buffer
D. a format string attack
Answer: C

Question: _____________ can modify data on your system – so that your system doesn’t run correctly or you can no longer access specific data, or it may even ask for ransom in order to give your access.
A. IM – Trojans
B. Backdoor Trojans
C. Trojan-Downloader
D. Ransom Trojan
Answer: D

Question: {Exam_Question}
{Exam_Choices}
Answer: """

FEW_SHOT_TEMPLATE_MMLU_NO_WHITESPACE = """
The following are multiple choice questions (with answers) about computer security.

Question: What is ethical hacking?
A. "Hacking" ethics so they justify unintended selfish behavior
B. Hacking systems (e.g., during penetration testing) to expose vulnerabilities so they can be fixed, rather than exploited
C. Hacking into systems run by those whose ethics you disagree with
D. A slang term for rapid software development, e.g., as part of hackathons
Answer:B

Question: The ____________ is anything which your search engine cannot search.
A. Haunted web
B. World Wide Web
C. Surface web
D. Deep Web
Answer:D

Question: SHA-1 has a message digest of
A. 160 bits
B. 512 bits
C. 628 bits
D. 820 bits
Answer:A

Question: Exploitation of the Heartbleed bug permits
A. overwriting cryptographic keys in memory
B. a kind of code injection
C. a read outside bounds of a buffer
D. a format string attack
Answer:C

Question: _____________ can modify data on your system – so that your system doesn’t run correctly or you can no longer access specific data, or it may even ask for ransom in order to give your access.
A. IM – Trojans
B. Backdoor Trojans
C. Trojan-Downloader
D. Ransom Trojan
Answer:D

Question: {Exam_Question}
{Exam_Choices}
Answer:"""

FEW_SHOT_TEMPLATE_MMLU_NO_WHITESPACE_AT_EXCEPTED_ANW = """
The following are multiple choice questions (with answers) about computer security.

Question: What is ethical hacking?
A. "Hacking" ethics so they justify unintended selfish behavior
B. Hacking systems (e.g., during penetration testing) to expose vulnerabilities so they can be fixed, rather than exploited
C. Hacking into systems run by those whose ethics you disagree with
D. A slang term for rapid software development, e.g., as part of hackathons
Answer: B

Question: The ____________ is anything which your search engine cannot search.
A. Haunted web
B. World Wide Web
C. Surface web
D. Deep Web
Answer: D

Question: SHA-1 has a message digest of
A. 160 bits
B. 512 bits
C. 628 bits
D. 820 bits
Answer: A

Question: Exploitation of the Heartbleed bug permits
A. overwriting cryptographic keys in memory
B. a kind of code injection
C. a read outside bounds of a buffer
D. a format string attack
Answer: C

Question: _____________ can modify data on your system – so that your system doesn’t run correctly or you can no longer access specific data, or it may even ask for ransom in order to give your access.
A. IM – Trojans
B. Backdoor Trojans
C. Trojan-Downloader
D. Ransom Trojan
Answer: D

Question: {Exam_Question}
{Exam_Choices}
Answer:"""


MMLU_PRO = """The following are multiple choice questions (with answers) about computer security. Think step by step and then finish your answer with "the answer is (X)" where X is the correct letter choice.

Question: {Exam_Question}
{Exam_Choices}
"""

### COMPUTER SCIENCE TEMPLATE, not usable for now
LLAMA31_INSTRUCT_MMLU_PRO_5_SHOT_COT_RAW="""<|start_header_id|>user<|end_header_id|>

Given the following question and candidate answers, choose the best answer.
Question: For a stationary autoregressive process, shocks will
A. Never occur
B. Persist indefinitely
C. Cause a permanent change in the trend
D. Grow exponentially
E. Only affect the next period
F. Eventually die away
G. Cause the process to become non-stationary
H. Immediately disappear
I. Lead to a cyclical pattern
J. Be balanced out by subsequent shocks

Your response should end with \"The best answer is [the_answer_letter].\" where the [the_answer_letter] is a letter from the provided choices.

Let's think step by step.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

We refer to Wikipedia articles on econometrics for help. This is a formal logic problem about stationally process. For a stationary autoregressive process, shocks will eventually die away. The best answer is F.<|eot_id|><|start_header_id|>user<|end_header_id|>

Given the following question and candidate answers, choose the best answer.
Question: Consider the following AR(1) model with the disturbances having zero mean and unit variance
yt = 0.2 + 0.4 yt-1 + ut
The (unconditional) mean of y will be given by
A. 0.45
B. 0.2
C. 0.4
D. 0.1
E. 0.3
F. 0.55
G. 0.25
H. 0.33
I. 0.6
J. 0.5

Your response should end with \"The best answer is [the_answer_letter].\" where the [the_answer_letter] is a letter from the provided choices.

Let's think step by step.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

We refer to Wikipedia articles on econometrics for help. Let’s solve this problem step by step. If we have a an AR(1) model with the disturbances having zero mean and unit variance, then the unconditional mean of y is equal to the following:
unconditional mean of y = (the intercept term) / (1 - autoregressive coefficient)
We know that the intercept term is 0.2 and the autoregressive coefficient is 0.4; thus, we have:
unconditional mean of y = (0.2) / (1 - 0.4) = (0.2) / (0.6) = 2 / 6 = 1 / 3, which is approximately 0.33. That means that the answer should be (H) 0.33. The best answer is H.<|eot_id|><|start_header_id|>user<|end_header_id|>

Given the following question and candidate answers, choose the best answer.
Question: Suppose that a test statistic has associated with it a p-value of 0.08. Which one of the following statements is true?
(i) If the size of the test were exactly 8%, we would be indifferent between rejecting and not rejecting the null hypothesis
(ii) The null would be rejected if a 10% size of test were used
(iii) The null would not be rejected if a 1% size of test were used
(iv) The null would be rejected if a 5% size of test were used.
A. (iii) and (iv) only
B. (i) and (iv) only
C. (i), (ii), and (iii) only
D. (i) and (ii) only
E. (i) and (iii) only
F. (i), (ii), (iii), and (iv).
G. (ii), (iii), and (iv) only
H. (ii) and (iii) only
I. (ii) and (iv) only
J. (i), (iii), and (iv) only

Your response should end with \"The best answer is [the_answer_letter].\" where the [the_answer_letter] is a letter from the provided choices.

Let's think step by step.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

We refer to Wikipedia articles on econometrics for help. Let’s reason about each of the options.
(i) is a true statement.
(ii) is a true statement.
(iii) is a true statement.
(iv) is not a true statement. Thus, (i), (ii), and (iii) are true. The best answer is C.<|eot_id|><|start_header_id|>user<|end_header_id|>

Given the following question and candidate answers, choose the best answer.
Question: Which of the following policies best describes supply-side fiscal policy?
A. Higher taxes on household income
B. Increased government spending
C. Increased taxes on corporate profits
D. Increased import tariffs
E. Decreased interest rates
F. Lower taxes on consumer goods
G. Lower taxes on research and development of new technology
H. Reduced government spending
I. Higher taxes on capital gains
J. An increase in the money supply

Your response should end with \"The best answer is [the_answer_letter].\" where the [the_answer_letter] is a letter from the provided choices.

Let's think step by step.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

We refer to Wikipedia articles on macroeconomics for help. Supply-side fiscal policy stimulates the economy by encouraging more production of goods and services through reduction in taxes and deregulation. The best answer is G.<|eot_id|><|start_header_id|>user<|end_header_id|>

Given the following question and candidate answers, choose the best answer.
Question: The concentration ratio for a monopoly is
A. 50
B. 5
C. 10
D. 90
E. 15
F. 100
G. 0
H. 25
I. 75
J. N/A

Your response should end with \"The best answer is [the_answer_letter].\" where the [the_answer_letter] is a letter from the provided choices.

Let's think step by step.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

We refer to Wikipedia articles on microeconomics for help. The concentration ratio is calculated as the sum of market share of a specific number of largest companies. Monopoly means one company or entity controls the entire market, therefore, the concentration ratio is 100 percent. The best answer is F.<|eot_id|><|start_header_id|>user<|end_header_id|>

Given the following question and candidate answers, choose the best answer.
Question: When the price of pears increases, we expect the following:
A. Quantity supplied of pears falls.
B. The price of apples falls.
C. There is no change in the quantity demanded or supplied.
D. The price of pears falls.
E. Quantity demanded of pears falls.
F. There is a surplus of pears in the market.
G. Quantity demanded of pears rises.
H. Demand for pears falls.
I. Quantity supplied of pears rises.
J. Demand for pears rises.

Your response should end with \"The best answer is [the_answer_letter].\" where the [the_answer_letter] is a letter from the provided choices.

Let's think step by step.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

"""

#https://huggingface.co/datasets/meta-llama/Meta-Llama-3.1-405B-Instruct-evals/viewer/Meta-Llama-3.1-405B-Instruct-evals__mmlu__details/latest?q=computer_security&row=11473
LLAMA31_INSTRUCT_MMLU_0_SHOT_COT_RAW = """<|start_header_id|>user<|end_header_id|>

Given the following question and four candidate answers (A, B, C and D), choose the best answer.

Question: {Exam_Question}
{Exam_Choices}

- For simple problems:
Directly provide the answer with minimal explanation.

- For complex problems:
Use this step-by-step format:
## Step 1: [Concise description]
[Brief explanation]
## Step 2: [Concise description]
[Brief explanation]

Regardless of the approach, always conclude with:
The best answer is [the_answer_letter].
where the [the_answer_letter] is one of A, B, C or D.

Let's think step by step.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

"""


LLAMA31_INSTRUCT_CC_0_SHOT_COT = """The following are multiple choice questions (with answers), choose the best answer.

Question: {Exam_Question}
{Exam_Choices}

- For simple problems:
Directly provide the answer with minimal explanation.

- For complex problems:
Use this step-by-step format:
## Step 1: [Concise description]
[Brief explanation]
## Step 2: [Concise description]
[Brief explanation]

Regardless of the approach, always conclude with:
The best answer is [the_answer_letter(s)].
where the [the_answer_letter(s)] is one or multiple of A, B, C, D, E, F...

Let's think step by step."""

LLAMA31_INSTRUCT_MMLU_5_SHOT_RAW = """<|start_header_id|>user<|end_header_id|>

Given the following question and four candidate answers (A, B, C and D), choose the best answer.
Question: For which of these two scenarios does the main character (who uses I/me/my) do something clearly morally wrong, according to ordinary moral standards in the US as of 2020? Scenario 1 | I really loved my newborn baby boy. Scenario 2 | The new girl is embarrassed to live in a trailer park, so I invite the class to her house.
A. Wrong, Wrong
B. Wrong, Not wrong
C. Not wrong, Wrong
D. Not wrong, Not wrong
Your response should end with \"The best answer is [the_answer_letter]\" where the [the_answer_letter] is one of A, B, C or D.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

The best answer is C.<|eot_id|><|start_header_id|>user<|end_header_id|>

Given the following question and four candidate answers (A, B, C and D), choose the best answer.
Question: For which of these two scenarios does the main character (who uses I/me/my) do something clearly morally wrong, according to ordinary moral standards in the US as of 2020? Scenario 1 | I asked for a cigarette from the guy outside the store. Scenario 2 | When the security guard left his post, I pocketed a rare coin.
A. Wrong, Wrong
B. Wrong, Not wrong
C. Not wrong, Wrong
D. Not wrong, Not wrong
Your response should end with \"The best answer is [the_answer_letter]\" where the [the_answer_letter] is one of A, B, C or D.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

The best answer is C.<|eot_id|><|start_header_id|>user<|end_header_id|>

Given the following question and four candidate answers (A, B, C and D), choose the best answer.
Question: For which of these two scenarios does the main character (who uses I/me/my) do something clearly morally wrong, according to ordinary moral standards in the US as of 2020? Scenario 1 | I bought an old pick-up truck for work. Scenario 2 | I looked up at the gorgeous waterfall and threw a rock at it.
A. Wrong, Wrong
B. Wrong, Not wrong
C. Not wrong, Wrong
D. Not wrong, Not wrong
Your response should end with \"The best answer is [the_answer_letter]\" where the [the_answer_letter] is one of A, B, C or D.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

The best answer is D.<|eot_id|><|start_header_id|>user<|end_header_id|>

Given the following question and four candidate answers (A, B, C and D), choose the best answer.
Question: For which of these two scenarios does the main character (who uses I/me/my) do something clearly morally wrong, according to ordinary moral standards in the US as of 2020? Scenario 1 | During the house's demolition, I pushed him into a wall. Scenario 2 | When I choose a babysitter for my twin nieces, I don't care about her racial background.
A. Wrong, Wrong
B. Wrong, Not wrong
C. Not wrong, Wrong
D. Not wrong, Not wrong
Your response should end with \"The best answer is [the_answer_letter]\" where the [the_answer_letter] is one of A, B, C or D.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

The best answer is B.<|eot_id|><|start_header_id|>user<|end_header_id|>

Given the following question and four candidate answers (A, B, C and D), choose the best answer.
Question: For which of these two scenarios does the main character (who uses I/me/my) do something clearly morally wrong, according to ordinary moral standards in the US as of 2020? Scenario 1 | I took his wallet after he harassed me at the bar. Scenario 2 | I made love to my newborn baby boy.
A. Wrong, Wrong
B. Wrong, Not wrong
C. Not wrong, Wrong
D. Not wrong, Not wrong
Your response should end with \"The best answer is [the_answer_letter]\" where the [the_answer_letter] is one of A, B, C or D.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

The best answer is A.<|eot_id|><|start_header_id|>user<|end_header_id|>

Given the following question and four candidate answers (A, B, C and D), choose the best answer.
Question: {Exam_Question}
{Exam_Choices}
Your response should end with \"The best answer is [the_answer_letter]\" where the [the_answer_letter] is one of A, B, C or D.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

The best answer is"""

LLAMA31_INSTRUCT_MMLU_5_SHOT_OPENAI =  [

   {"role": "user", "content": """Given the following question and four candidate answers (A, B, C and D), choose the best answer.
Question: SHA-1 has a message digest of
A. 160 bits
B. 512 bits
C. 628 bits
D. 820 bits
Your response should end with \"The best answer is [the_answer_letter]\" where the [the_answer_letter] is one of A, B, C or D."""},

    {"role": "assistant", "content": "The best answer is A."},
    {"role": "user", "content": """Given the following question and four candidate answers (A, B, C and D), choose the best answer.
Question: _____________ can modify data on your system – so that your system doesn’t run correctly or you can no longer access specific data, or it may even ask for ransom in order to give your access.
A. IM – Trojans
B. Backdoor Trojans
C. Trojan-Downloader
D. Ransom Trojan
Your response should end with \"The best answer is [the_answer_letter]\" where the [the_answer_letter] is one of A, B, C or D."""},

   {"role": "assistant", "content": "The best answer is D."},
   {"role": "user", "content": """Given the following question and four candidate answers (A, B, C and D), choose the best answer.
Question: What is ethical hacking?
A. \"Hacking\" ethics so they justify unintended selfish behavior
B. Hacking systems (e.g., during penetration testing) to expose vulnerabilities so they can be fixed, rather than exploited
C. Hacking into systems run by those whose ethics you disagree with
D. A slang term for rapid software development, e.g., as part of hackathons
Your response should end with \"The best answer is [the_answer_letter]\" where the [the_answer_letter] is one of A, B, C or D."""},

   {"role": "assistant", "content": "The best answer is B."},
   {"role": "user", "content": """Given the following question and four candidate answers (A, B, C and D), choose the best answer.
Question: Exploitation of the Heartbleed bug permits
A. overwriting cryptographic keys in memory
B. a kind of code injection
C. a read outside bounds of a buffer
D. a format string attack
Your response should end with \"The best answer is [the_answer_letter]\" where the [the_answer_letter] is one of A, B, C or D."""},

   {"role": "assistant", "content": "The best answer is C."},
   {"role": "user", "content": """Given the following question and four candidate answers (A, B, C and D), choose the best answer.
Question: The ____________ is anything which your search engine cannot search.
A. Haunted web
B. World Wide Web
C. Surface web
D. Deep Web
Your response should end with \"The best answer is [the_answer_letter]\" where the [the_answer_letter] is one of A, B, C or D."""},

   {"role": "assistant", "content": "The best answer is D."},
   {"role": "user", "content": """Given the following question and four candidate answers (A, B, C and D), choose the best answer.
Question: {Exam_Question}
{Exam_Choices}
Your response should end with \"The best answer is [the_answer_letter]\" where the [the_answer_letter] is one of A, B, C or D."""},
{"role": "assistant", "content": "The best answer is"},
]

LLAMA31_INSTRUCT_CCNA_5_SHOT_OPENAI =  [

   {"role": "user", "content": """The following are multiple choice questions (with answers) about network fundamentals, network access, security fundamentals, automation and programmability.
Question: Which two options are the best reasons to use an IPV4 private IP space? (Choose two.)
A. to enable intra-enterprise communication
B. to implement NAT
C. to connect applications
D. to conserve global address space
E. to manage routing overhead
Your response should end with \"The best answer is [the_answer_letter(s)]\" where the [the_answer_letter(s)] is/are of A, B, C, D, E, F,..."""},

    {"role": "assistant", "content": "The best answer is AD."},
    {"role": "user", "content": """The following are multiple choice questions (with answers) about network fundamentals, network access, security fundamentals, automation and programmability.
Question: Security Group Access requires which three syslog messages to be sent to Cisco ISE? (Choose three.)
A. IOS-7-PROXY_DROP
B. AP-1-AUTH_PROXY_DOS_ATTACK
C. MKA-2-MACDROP
D. AUTHMGR-5-MACMOVE
E. ASA-6-CONNECT_BUILT
F. AP-1-AUTH_PROXY_FALLBACK_REQ
Your response should end with \"The best answer is [the_answer_letter(s)]\" where the [the_answer_letter(s)] is/are of A, B, C, D, E, F,..."""},

   {"role": "assistant", "content": "The best answer is BDF."},
   {"role": "user", "content": """The following are multiple choice questions (with answers) about network fundamentals, network access, security fundamentals, automation and programmability.
Question: Which two authentication stores are supported to design a wireless network using PEAP EAP-MSCHAPv2 as the authentication method? (Choose two.)
A. Microsoft Active Directory
B. ACS
C. LDAP
D. RSA Secure-ID
E. Certificate Server
Your response should end with \"The best answer is [the_answer_letter(s)]\" where the [the_answer_letter(s)] is/are of A, B, C, D, E, F,..."""},

   {"role": "assistant", "content": "The best answer is AB."},
   {"role": "user", "content": """The following are multiple choice questions (with answers) about network fundamentals, network access, security fundamentals, automation and programmability.
Question: The corporate security policy requires multiple elements to be matched in an authorization policy. Which elements can be combined to meet the requirement?
A. Device registration status and device activation status
B. Network access device and time condition
C. User credentials and server certificate
D. Built-in profile and custom profile
Your response should end with \"The best answer is [the_answer_letter(s)]\" where the [the_answer_letter(s)] is/are of A, B, C, D, E, F,..."""},

   {"role": "assistant", "content": "The best answer is B."},
   {"role": "user", "content": """The following are multiple choice questions (with answers) about network fundamentals, network access, security fundamentals, automation and programmability.
Question: Which three posture states can be used for authorization rules? (Choose three.)
A. unknown
B. known
C. noncompliant
D. quarantined
E. compliant
F. no access
G. limited
Your response should end with \"The best answer is [the_answer_letter(s)]\" where the [the_answer_letter(s)] is/are of A, B, C, D, E, F,..."""},

   {"role": "assistant", "content": "The best answer is ACE."},
   {"role": "user", "content": """The following are multiple choice questions (with answers) about network fundamentals, network access, security fundamentals, automation and programmability.
Question: {Exam_Question}
{Exam_Choices}
Your response should end with \"The best answer is [the_answer_letter(s)]\" where the [the_answer_letter(s)] is/are of A, B, C, D, E, F,..."""},
{"role": "assistant", "content": "The best answer is"},
]

LLAMA31_INSTRUCT_CCNA_5_SHOT_RAW =  """<|start_header_id|>user<|end_header_id|>

The following are multiple choice questions (with answers) about network fundamentals, network access, security fundamentals, automation and programmability.
Question: Which two options are the best reasons to use an IPV4 private IP space? (Choose two.)
A. to enable intra-enterprise communication
B. to implement NAT
C. to connect applications
D. to conserve global address space
E. to manage routing overhead
Your response should end with \"The best answer is [the_answer_letter(s)]\" where the [the_answer_letter(s)] is/are of A, B, C, D, E, F,...
<|eot_id|><|start_header_id|>assistant<|end_header_id|>

The best answer is AD.<|eot_id|><|start_header_id|>user<|end_header_id|>

The following are multiple choice questions (with answers) about network fundamentals, network access, security fundamentals, automation and programmability.
Question: Security Group Access requires which three syslog messages to be sent to Cisco ISE? (Choose three.)
A. IOS-7-PROXY_DROP
B. AP-1-AUTH_PROXY_DOS_ATTACK
C. MKA-2-MACDROP
D. AUTHMGR-5-MACMOVE
E. ASA-6-CONNECT_BUILT
F. AP-1-AUTH_PROXY_FALLBACK_REQ
Your response should end with \"The best answer is [the_answer_letter(s)]\" where the [the_answer_letter(s)] is/are of A, B, C, D, E, F,...
<|eot_id|><|start_header_id|>assistant<|end_header_id|>

The best answer is BDF.<|eot_id|><|start_header_id|>user<|end_header_id|>

The following are multiple choice questions (with answers) about network fundamentals, network access, security fundamentals, automation and programmability.
Question: Which two authentication stores are supported to design a wireless network using PEAP EAP-MSCHAPv2 as the authentication method? (Choose two.)
A. Microsoft Active Directory
B. ACS
C. LDAP
D. RSA Secure-ID
E. Certificate Server
Your response should end with \"The best answer is [the_answer_letter(s)]\" where the [the_answer_letter(s)] is/are of A, B, C, D, E, F,...
<|eot_id|><|start_header_id|>assistant<|end_header_id|>

The best answer is AB.<|eot_id|><|start_header_id|>user<|end_header_id|>

The following are multiple choice questions (with answers) about network fundamentals, network access, security fundamentals, automation and programmability.
Question: The corporate security policy requires multiple elements to be matched in an authorization policy. Which elements can be combined to meet the requirement?
A. Device registration status and device activation status
B. Network access device and time condition
C. User credentials and server certificate
D. Built-in profile and custom profile
Your response should end with \"The best answer is [the_answer_letter(s)]\" where the [the_answer_letter(s)] is/are of A, B, C, D, E, F,...
<|eot_id|><|start_header_id|>assistant<|end_header_id|>

The best answer is B.<|eot_id|><|start_header_id|>user<|end_header_id|>

The following are multiple choice questions (with answers) about network fundamentals, network access, security fundamentals, automation and programmability.
Question: Which three posture states can be used for authorization rules? (Choose three.)
A. unknown
B. known
C. noncompliant
D. quarantined
E. compliant
F. no access
G. limited
Your response should end with \"The best answer is [the_answer_letter(s)]\" where the [the_answer_letter(s)] is/are of A, B, C, D, E, F,...
<|eot_id|><|start_header_id|>assistant<|end_header_id|>

The best answer is ACE.<|eot_id|><|start_header_id|>user<|end_header_id|>

The following are multiple choice questions (with answers) about network fundamentals, network access, security fundamentals, automation and programmability.
Question: {Exam_Question}
{Exam_Choices}
Your response should end with \"The best answer is [the_answer_letter(s)]\" where the [the_answer_letter(s)] is/are of A, B, C, D, E, F,....<|eot_id|><|start_header_id|>assistant<|end_header_id|>

The best answer is"""

LLAMA31_INSTRUCT_CC_5_SHOT_OPENAI =  [

   {"role": "user", "content": """The following are multiple choice questions (with answers).
Question: Which two options are the best reasons to use an IPV4 private IP space? (Choose two.)
A. to enable intra-enterprise communication
B. to implement NAT
C. to connect applications
D. to conserve global address space
E. to manage routing overhead
Your response should end with \"The best answer is [the_answer_letter(s)]\" where the [the_answer_letter(s)] is/are of A, B, C, D, E, F,..."""},

    {"role": "assistant", "content": "The best answer is AD."},
    {"role": "user", "content": """The following are multiple choice questions (with answers).
Question: Security Group Access requires which three syslog messages to be sent to Cisco ISE? (Choose three.)
A. IOS-7-PROXY_DROP
B. AP-1-AUTH_PROXY_DOS_ATTACK
C. MKA-2-MACDROP
D. AUTHMGR-5-MACMOVE
E. ASA-6-CONNECT_BUILT
F. AP-1-AUTH_PROXY_FALLBACK_REQ
Your response should end with \"The best answer is [the_answer_letter(s)]\" where the [the_answer_letter(s)] is/are of A, B, C, D, E, F,..."""},

   {"role": "assistant", "content": "The best answer is BDF."},
   {"role": "user", "content": """The following are multiple choice questions (with answers).
Question: Which two authentication stores are supported to design a wireless network using PEAP EAP-MSCHAPv2 as the authentication method? (Choose two.)
A. Microsoft Active Directory
B. ACS
C. LDAP
D. RSA Secure-ID
E. Certificate Server
Your response should end with \"The best answer is [the_answer_letter(s)]\" where the [the_answer_letter(s)] is/are of A, B, C, D, E, F,..."""},

   {"role": "assistant", "content": "The best answer is AB."},
   {"role": "user", "content": """The following are multiple choice questions (with answers).
Question: The corporate security policy requires multiple elements to be matched in an authorization policy. Which elements can be combined to meet the requirement?
A. Device registration status and device activation status
B. Network access device and time condition
C. User credentials and server certificate
D. Built-in profile and custom profile
Your response should end with \"The best answer is [the_answer_letter(s)]\" where the [the_answer_letter(s)] is/are of A, B, C, D, E, F,..."""},

   {"role": "assistant", "content": "The best answer is B."},
   {"role": "user", "content": """The following are multiple choice questions (with answers).
Question: Which three posture states can be used for authorization rules? (Choose three.)
A. unknown
B. known
C. noncompliant
D. quarantined
E. compliant
F. no access
G. limited
Your response should end with \"The best answer is [the_answer_letter(s)]\" where the [the_answer_letter(s)] is/are of A, B, C, D, E, F,..."""},

   {"role": "assistant", "content": "The best answer is ACE."},
   {"role": "user", "content": """The following are multiple choice questions (with answers).
Question: {Exam_Question}
{Exam_Choices}
Your response should end with \"The best answer is [the_answer_letter(s)]\" where the [the_answer_letter(s)] is/are of A, B, C, D, E, F,..."""},
{"role": "assistant", "content": "The best answer is"},
]