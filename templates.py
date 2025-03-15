MMLU_SIMPLE = """The following are multiple choice questions (with answers) about computer security. Finish your answer with "the answer is (X)" where X is the correct letter choice.

Question: {Exam_Question}
{Exam_Choices}
"""

MMLU_PRO = """The following are multiple choice questions (with answers) about computer security. Think step by step and then finish your answer with "the answer is (X)" where X is the correct letter choice.

Question: {Exam_Question}
{Exam_Choices}
"""

LLAMA31_MMLU_PRO_5_SHOT_COT = [
    { "role": "user", "content": """Given the following question and ten candidate answers (A, B, C, D, E, F, G, H, I, and J), choose the best answer.
Question: A certain pipelined RISC machine has 8 general-purpose registers R0, R1, . . . , R7 and supports the following operations:
ADD Rs1, Rs2, Rd (Add Rs1 to Rs2 and put the sum in Rd)  
MUL Rs1, Rs2, Rd (Multiply Rs1 by Rs2 and put the product in Rd)  
An operation normally takes one cycle; however, an operation takes two cycles if it produces a result required by the immediately following operation in an operation sequence.  

Consider the expression AB + ABC + BC, where variables A, B, C are located in registers R0, R1, R2. If the contents of these three registers must not be modified, what is the minimum number of clock cycles required for an operation sequence that computes the value of AB + ABC + BC?

A. 10 cycles  
B. 6 cycles  
C. 9 cycles  
D. 53 cycles  
E. 12 cycles  
F. 4 cycles  
G. 7 cycles  
H. 8 cycles  
I. N/A  
J. N/A  

Your response should end with \"The best answer is [the_answer_letter]\" where the [the_answer_letter] is one of A, B, C, D, E, F, G, H, I, or J."""
    },
    {"role": "assistant", "content": """Let's think step by step. First, we are given that A is in R0, B is in R1, and C is in R2.
Next, we can see that we must compute three multiplies (AB, BC, and ABC) and two adds (AB + ABC, (AB + ABC) + BC) to compute our final answer, resulting in a minimum of five clock cycles.
Next, we can see that there is no way to avoid at least one pipeline stall when computing our final answer, because to compute our final sum we must wait at least one cycle for the results from the previous stage to be ready. Thus, our minimum number of cycles must be 6.
We can verify that we can create a solution that requires only six cycles as follows:
compute AB: MUL R0, R1, R3
compute BC: MUL R1, R2, R4
compute ABC: MUL R3, R4, R5
compute AB + BC: ADD R3, R4, R6
STALL
compute AB + ABC + BC: ADD R5, R6, R7
So there are 6 cycles. The answer is B."""},
   {"role": "user", "content": """Given the following question and ten candidate answers (A, B, C, D, E, F, G, H, I, and J), choose the best answer.
Question: A compiler generates code for the following assignment statement.
G := (A + B) * C - (D + E) * F
The target machine has a single accumulator and a single-address instruction set consisting of instructions load, store, add, subtract, and multiply. For the arithmetic operations, the left operand is taken from the accumulator and the result appears in the accumulator. The smallest possible number of instructions in the resulting code is:

A. 55 instructions  
B. 53 instructions  
C. 12 instructions  
D. 52 instructions  
E. 11 instructions  
F. 54 instructions  
G. 56 instructions  
H. 10 instructions  
I. 57 instructions  
J. 51 instructions  

Your response should end with \"The best answer is [the_answer_letter]\" where the [the_answer_letter] is one of A, B, C, D, E, F, G, H, I, or J."""
},
   {"role": "assistant", "content": """Let's think step by step. We can compute the final answer with the following sequence of operations:
1. LOAD D  (accumulator = D)
2. ADD E  (accumulator = D+E)
3. MUL F  (accumulator = (D+E)*F)
4. STORE X (X = (D+E)*F)
5. LOAD A  (accumulator = A)
6. ADD B  (accumulator = A+B)
7. MUL C  (accumulator = (A+B)*C)
8. SUB X  (accumulator = (A+B)*C - (D+E)*F)
9. STORE G (G = (A+B)*C - (D+E)*F)
This sequence takes 9 instructions. The answer is I.
"""},

   {"role": "user","content": """Given the following question and ten candidate answers (A, B, C, D, E, F, G, H, I, and J), choose the best answer.
Question: SHA-1 has a message digest of

A. 628 bits  
B. 780 bits  
C. 160 bits  
D. 256 bits  
E. 2048 bits  
F. 820 bits  
G. 128 bits  
H. 512 bits  
I. 1024 bits  
J. 64 bits  

Your response should end with \"The best answer is [the_answer_letter]\" where the [the_answer_letter] is one of A, B, C, D, E, F, G, H, I, or J."""
   },
   {"role": "assistant", "content": """A: Let's think step by step. Since SHA-1 is a hash function which takes an input and produces a 160-bit (20-byte) hash value, its message digest is 160 bits. 
   The answer is C."""},

   {"role": "user", "content": """Given the following question and ten candidate answers (A, B, C, D, E, F, G, H, I, and J), choose the best answer.
Question: _____________ can modify data on your system – so that your system doesn’t run correctly or you can no longer access specific data, or it may even ask for ransom in order to give you access.

A. Email Trojans  
B. Backdoor Trojans  
C. Rootkit Trojans  
D. Banking Trojans  
E. Trojan-Downloader  
F. Spyware Trojans  
G. Network Trojans  
H. Worm Trojans  
I. Ransom Trojans  
J. IM Trojans  

Your response should end with \"The best answer is [the_answer_letter]\" where the [the_answer_letter] is one of A, B, C, D, E, F, G, H, I, or J."""},
   {"role": "assistant", "content": """A: Let's think step by step. The system is asking for trojans, which are for ransom, which means ransom trojan. 
   The answer is I."""},

    {"role": "user", "content": """Given the following question and ten candidate answers (A, B, C, D, E, F, G, H, I, and J), choose the best answer.
Question: In the program below, the initial value of X is 5 and the initial value of Y is 10.
IF (X < 0){
 DISPLAY (\"Foxtrot\")
} ELSE {
 IF (X > Y){
  DISPLAY (\"Hotel\")
 } ELSE {
  IF (Y > 0){
   DISPLAY (\"November\")
  } ELSE {
   DISPLAY (\"Yankee\")
  }
 }
}
What is displayed as a result of running the program?

A. November  
B. Foxtrot  
C. Zulu  
D. Alpha  
E. Charlie  
F. Bravo  
G. Yankee  
H. Echo  
I. Hotel  
J. Delta  

Your response should end with \"The best answer is [the_answer_letter]\" where the [the_answer_letter] is one of A, B, C, D, E, F, G, H, I, or J."""},
    {"role": "assistant", "content": """A: Let's think step by step. Because X has the value 5, the first conditional IF (X < 0) is false, so we move to the first ELSE clause. Because X is 5 and Y is 10, the second conditional IF (X > Y) is false, so we move to the following ELSE clause. Since Y is 10, the conditional IF (Y > 0) is true, so the command DISPLAY ("November") is executed. 
   The answer is A."""},
]

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

LLAMA31_INSTRUCT_0_SHOT_OPENAI =  [
   {"role": "user", "content": """The following are multiple choice questions (with answers).
Question: {Exam_Question}
{Exam_Choices}
Your response should end with \"The best answer is [the_answer_letter(s)]\" where the [the_answer_letter(s)] is/are of A, B, C, D, E,.."""},

]