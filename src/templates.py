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