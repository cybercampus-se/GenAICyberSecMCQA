MMLU_PRO = """The following are multiple choice questions (with answers) about computer security. Think step by step and then finish your answer with "the answer is (X)" where X is the correct letter choice.

Question: {Exam_Question}
{Exam_Choices}
"""

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
