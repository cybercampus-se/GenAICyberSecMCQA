FEW_SHOT_TEMPLATE = """
    The following are multiple choice questions (with answers) about network fundamentals, network access,
    security fundamentals, automation and programmability. Here are four examples:
    
    Question: Which two options are the best reasons to use an IPV4 private IP space? (Choose two.)
    
    Choices:
    A. to enable intra-enterprise communication
    B. to implement NAT
    C. to connect applications
    D. to conserve global address space
    E. to manage routing overhead
                                               
    Correct Answer: ['A','D']

    Question: Security Group Access requires which three syslog messages to be sent to Cisco ISE? (Choose three.)
    A. IOS-7-PROXY_DROP
    B. AP-1-AUTH_PROXY_DOS_ATTACK
    C. MKA-2-MACDROP
    D. AUTHMGR-5-MACMOVE
    E. ASA-6-CONNECT_BUILT
    F. AP-1-AUTH_PROXY_FALLBACK_REQ

    Correct Answer: ['B', 'D', 'F']

    Question: Which two authentication stores are supported to design a wireless network using PEAP EAP-MSCHAPv2 as the authentication method? (Choose two.)
    A. Microsoft Active Directory
    B. ACS
    C. LDAP
    D. RSA Secure-ID
    E. Certificate Server
    
    Correct Answer: ['A', 'B']

    Question:The corporate security policy requires multiple elements to be matched in an authorization policy. Which elements can be combined to meet the requirement?
    A. Device registration status and device activation status
    B. Network access device and time condition
    C. User credentials and server certificate
    D. Built-in profile and custom profile

    Correct Answer: ['B']

    Question:Which three posture states can be used for authorization rules? (Choose three.)
    A. unknown
    B. known
    C. noncompliant
    D. quarantined
    E. compliant
    F. no access
    G. limited

    Correct Answer: ['A', 'C', 'E']

    
    Please give the answer in the following format:
        Correct Answer: ['A','D']           
    
    Now, answer the following question:
    Question: {Exam_Question}        
                    
    Choices:
    {Exam_Choices}
    """