import os
import re
from flask import Flask, render_template_string, request
import pdfplumber

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Comprehensive 22-Domain Taxonomy with Sub-domains, Skills, Certifications & Day-by-Day Roadmaps
DOMAIN_TAXONOMY = {
    "cybersecurity": {
        "title": "Cybersecurity & Information Security",
        "subdomains": {
            "vapt": {"roles": ["Penetration Tester", "VAPT Engineer", "Ethical Hacker", "Web Security Analyst"], "skills": ["burp suite", "nmap", "metasploit", "owasp top 10", "sql injection", "python"]},
            "soc": {"roles": ["SOC Analyst L1", "SOC Analyst L2", "SOC Analyst L3", "Security Operations Engineer"], "skills": ["siem", "wireshark", "ids/ips", "incident response", "splunk", "log analysis"]},
            "appsec": {"roles": ["Application Security Engineer", "Product Security Engineer", "Secure Code Auditor"], "skills": ["sast", "dast", "secure coding", "api security", "java", "python"]},
            "dfir": {"roles": ["Digital Forensics Analyst", "Incident Response Analyst", "Malware Analyst"], "skills": ["autopsy", "volatility", "malware analysis", "forensics", "wireshark"]}
        },
        "core_skills": ["python", "linux", "wireshark", "nmap", "burp suite", "metasploit", "networking", "incident response", "vapt", "zero trust"],
        "certifications": ["CEH", "CompTIA Security+", "OSCP", "CTIGA", "CISSP"],
        "roadmap": [
            {
                "phase": "Phase 1 (Days 1 - 30)",
                "title": "Foundations & Linux Terminal",
                "focus": "Start here first! Master Linux CLI navigation, bash scripting, file permissions, and core Networking (TCP/IP model, OSI layers, DNS, Subnetting, ARP).",
                "action": "Once this is fully mastered and you can comfortably configure IPs and analyze ports, proceed to Phase 2."
            },
            {
                "phase": "Phase 2 (Days 31 - 60)",
                "title": "Network & Traffic Analysis",
                "focus": "Learn packet capture and traffic analysis using Wireshark, active reconnaissance with Nmap, and SIEM monitoring workflows.",
                "action": "After successfully analyzing handshake packets and detecting anomalies, move on to Phase 3."
            },
            {
                "phase": "Phase 3 (Days 61 - 100)",
                "title": "VAPT & Web Application Security",
                "focus": "Study the OWASP Top 10 vulnerabilities (SQLi, XSS, CSRF, IDOR). Perform hands-on penetration testing using Burp Suite and Metasploit.",
                "action": "Once you can successfully exploit and patch lab vulnerabilities, proceed to the final advanced phase."
            },
            {
                "phase": "Phase 4 (Days 101 - 150)",
                "title": "Advanced DFIR, Zero Trust & Certifications",
                "focus": "Dive into Digital Forensics & Incident Response (Autopsy/Volatility), Zero Trust architectures, and prepare for industry certifications (CEH/OSCP/CTIGA).",
                "action": "Complete capstone labs and apply for security roles with full confidence."
            }
        ]
    },
    "software_dev": {
        "title": "Software Development & Engineering",
        "subdomains": {
            "backend": {"roles": ["Software Engineer", "Software Developer", "Backend Developer", "API Developer", "Systems Developer"], "skills": ["python", "java", "node.js", "sql", "rest api", "git"]},
            "frontend": {"roles": ["Frontend Developer", "UI Developer"], "skills": ["react", "javascript", "html", "css", "typescript"]},
            "fullstack": {"roles": ["Full Stack Developer", "Application Developer"], "skills": ["react", "node.js", "mongodb", "express", "git"]}
        },
        "core_skills": ["react", "node.js", "mongodb", "javascript", "python", "sql", "git", "rest api", "java", "c++"],
        "certifications": ["AWS Certified Developer", "Oracle Certified Java Professional", "Meta Front-End Developer"],
        "roadmap": [
            {
                "phase": "Phase 1 (Days 1 - 30)",
                "title": "Programming Logic & Version Control",
                "focus": "Start with C++/Java/Python fundamentals, Data Structures & Algorithms, and Git version control workflows.",
                "action": "Once you solve 50+ DSA problems and master git commits, move to Phase 2."
            },
            {
                "phase": "Phase 2 (Days 31 - 70)",
                "title": "Frontend Development & UI",
                "focus": "Learn HTML5, CSS3, modern JavaScript (ES6+), and build responsive user interfaces using React.js.",
                "action": "After building 3 fully responsive web apps, proceed to Phase 3."
            },
            {
                "phase": "Phase 3 (Days 71 - 120)",
                "title": "Backend Architecture & Databases",
                "focus": "Build robust REST APIs using Node.js/Python, manage relational SQL databases and NoSQL (MongoDB), with secure JWT authentication.",
                "action": "Once backend communication and DB schemas are integrated, move to Phase 4."
            },
            {
                "phase": "Phase 4 (Days 121 - 150)",
                "title": "System Design & Cloud Deployment",
                "focus": "Study high-level system design, microservices, containerization with Docker, and cloud hosting.",
                "action": "Deploy your full-stack application live to complete your portfolio."
            }
        ]
    },
    "web_dev": {
        "title": "Web Development",
        "subdomains": {
            "web_general": {"roles": ["Web Developer", "Web Application Developer", "WordPress Developer"], "skills": ["html", "css", "javascript", "php", "wordpress", "mysql"]}
        },
        "core_skills": ["html", "css", "javascript", "php", "wordpress", "mysql", "git", "react"],
        "certifications": ["WordPress Expert Certification", "Frontend Master Certificate"],
        "roadmap": [
            {
                "phase": "Phase 1 (Days 1 - 30)",
                "title": "UI Fundamentals & Scripting",
                "focus": "Master semantic HTML, responsive CSS layouts, flexbox/grid, and core JavaScript DOM manipulation.",
                "action": "After building static landing pages, proceed to Phase 2."
            },
            {
                "phase": "Phase 2 (Days 31 - 60)",
                "title": "CMS & PHP Integration",
                "focus": "Learn WordPress theme & plugin customization, PHP fundamentals, and MySQL database configuration.",
                "action": "Once you build a custom live WordPress site, move to Phase 3."
            },
            {
                "phase": "Phase 3 (Days 61 - 90)",
                "title": "Advanced Web Frameworks & Security",
                "focus": "Integrate modern JavaScript frameworks, secure forms against XSS/CSRF, and optimize site performance.",
                "action": "Publish your portfolio and professional web projects."
            }
        ]
    },
    "mobile_dev": {
        "title": "Mobile Development",
        "subdomains": {
            "cross_native": {"roles": ["Android Developer", "iOS Developer", "Flutter Developer", "React Native Developer", "Mobile Application Developer"], "skills": ["flutter", "react native", "kotlin", "swift", "dart"]}
        },
        "core_skills": ["flutter", "react native", "kotlin", "swift", "dart", "java", "git"],
        "certifications": ["Google Associate Android Developer", "Apple Certified iOS Developer"],
        "roadmap": [
            {
                "phase": "Phase 1 (Days 1 - 35)",
                "title": "Core Mobile Language",
                "focus": "Start with Kotlin/Swift or Dart syntax, OOP principles, and mobile UI design fundamentals.",
                "action": "Once basic screen navigation is mastered, proceed to Phase 2."
            },
            {
                "phase": "Phase 2 (Days 36 - 80)",
                "title": "Cross-Platform Frameworks",
                "focus": "Learn Flutter widgets or React Native components, state management (Provider/Redux), and local storage.",
                "action": "After building 2 fully functional mobile apps, move to Phase 3."
            },
            {
                "phase": "Phase 3 (Days 81 - 110)",
                "title": "API Integration & App Store Deployment",
                "focus": "Connect REST APIs, handle push notifications, and prepare apps for Google Play Store / Apple App Store release.",
                "action": "Launch your mobile app live."
            }
        ]
    },
    "networking": {
        "title": "Networking & Infrastructure",
        "subdomains": {
            "net_ops": {"roles": ["Network Engineer", "Network Administrator", "Network Analyst", "NOC Engineer", "Network Support Engineer", "Network Architect"], "skills": ["tcp/ip", "routing", "switching", "wireshark", "cisco", "firewall"]}
        },
        "core_skills": ["tcp/ip", "routing", "switching", "wireshark", "cisco", "firewalls", "dns", "subnetting"],
        "certifications": ["CCNA", "CCNP", "CompTIA Network+"],
        "roadmap": [
            {
                "phase": "Phase 1 (Days 1 - 30)",
                "title": "Network Models & IP Addressing",
                "focus": "Master OSI and TCP/IP models, IPv4/IPv6 subnetting, CIDR notation, and Ethernet framing.",
                "action": "Once subnet calculations are seamless, move to Phase 2."
            },
            {
                "phase": "Phase 2 (Days 31 - 70)",
                "title": "Cisco Routing & Switching",
                "focus": "Configure Cisco routers and switches, VLANs, trunking, STP, and routing protocols (OSPF, EIGRP).",
                "action": "After simulating networks in Packet Tracer, proceed to Phase 3."
            },
            {
                "phase": "Phase 3 (Days 71 - 100)",
                "title": "Firewalls, VPNs & Enterprise Security",
                "focus": "Implement enterprise firewalls, ACLs, IPsec VPNs, and network troubleshooting.",
                "action": "Prepare for CCNA or Network+ certification exams."
            }
        ]
    },
    "cloud_devops": {
        "title": "Cloud, DevOps & SRE",
        "subdomains": {
            "devops_cloud": {"roles": ["Cloud Engineer", "Cloud Administrator", "Cloud Architect", "DevOps Engineer", "DevSecOps Engineer", "Platform Engineer", "Site Reliability Engineer", "Infrastructure Engineer"], "skills": ["aws", "docker", "kubernetes", "terraform", "ci/cd", "linux", "jenkins"]}
        },
        "core_skills": ["linux", "docker", "kubernetes", "aws", "terraform", "ci/cd", "jenkins", "python", "bash scripting"],
        "certifications": ["AWS Certified Solutions Architect", "CKA", "Terraform Associate"],
        "roadmap": [
            {
                "phase": "Phase 1 (Days 1 - 30)",
                "title": "Linux Administration & Bash",
                "focus": "Master Linux CLI, permissions, process management, SSH configurations, and Bash scripting.",
                "action": "Once comfortable managing Linux servers, move to Phase 2."
            },
            {
                "phase": "Phase 2 (Days 31 - 70)",
                "title": "Containerization & Cloud Basics",
                "focus": "Learn Docker container creation, image optimization, and AWS core services (EC2, S3, IAM, VPC).",
                "action": "After deploying containerized apps to AWS, proceed to Phase 3."
            },
            {
                "phase": "Phase 3 (Days 71 - 120)",
                "title": "Kubernetes & Infrastructure as Code",
                "focus": "Master Kubernetes cluster management (Pods, Deployments, Services) and Terraform for automated provisioning.",
                "action": "Once automated pipelines are built, move to Phase 4."
            },
            {
                "phase": "Phase 4 (Days 121 - 150)",
                "title": "CI/CD Pipelines & Monitoring",
                "focus": "Build automated GitHub Actions / Jenkins pipelines with security scanning and Prometheus/Grafana monitoring.",
                "action": "Earn cloud and DevOps certifications."
            }
        ]
    },
    "data_analytics": {
        "title": "Data & Analytics",
        "subdomains": {
            "data_science": {"roles": ["Data Analyst", "Data Engineer", "Data Scientist", "BI Analyst", "BI Developer", "Data Warehouse Engineer", "ETL Developer"], "skills": ["python", "sql", "pandas", "tableau", "power bi", "etl", "spark"]}
        },
        "core_skills": ["python", "sql", "pandas", "numpy", "tableau", "power bi", "etl", "statistics"],
        "certifications": ["Google Data Analytics Professional", "AWS Certified Data Analytics"],
        "roadmap": [
            {
                "phase": "Phase 1 (Days 1 - 30)",
                "title": "SQL & Spreadsheet Mastery",
                "focus": "Learn advanced SQL queries (Joins, CTEs, Window functions), data cleaning, and Excel analytics.",
                "action": "Once database querying is efficient, proceed to Phase 2."
            },
            {
                "phase": "Phase 2 (Days 31 - 70)",
                "title": "Python for Data Analysis",
                "focus": "Master Python libraries including Pandas, NumPy, Matplotlib, and Seaborn for Exploratory Data Analysis.",
                "action": "After cleaning complex datasets, move to Phase 3."
            },
            {
                "phase": "Phase 3 (Days 71 - 100)",
                "title": "Business Intelligence & Dashboards",
                "focus": "Build interactive executive dashboards using Tableau or Power BI and understand ETL data pipelines.",
                "action": "Present your analytical projects in a portfolio."
            }
        ]
    },
    "aiml": {
        "title": "AI & Machine Learning",
        "subdomains": {
            "artificial_intelligence": {"roles": ["AI Engineer", "Machine Learning Engineer", "ML Engineer", "NLP Engineer", "Computer Vision Engineer", "Generative AI Engineer", "LLM Engineer", "AI Research Engineer"], "skills": ["python", "pytorch", "tensorflow", "scikit-learn", "nlp", "computer vision", "llm", "rag"]}
        },
        "core_skills": ["python", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "nlp", "computer vision", "llm"],
        "certifications": ["TensorFlow Developer Certificate", "AWS Certified Machine Learning Specialty"],
        "roadmap": [
            {
                "phase": "Phase 1 (Days 1 - 35)",
                "title": "Math, Stats & Python Libraries",
                "focus": "Study linear algebra, calculus, probability statistics, and Python numerical libraries (NumPy, Pandas).",
                "action": "Once statistical foundations are clear, move to Phase 2."
            },
            {
                "phase": "Phase 2 (Days 36 - 80)",
                "title": "Classical Machine Learning",
                "focus": "Build supervised and unsupervised ML models (Regression, Decision Trees, SVM, Clustering) using Scikit-Learn.",
                "action": "After evaluating model performance metrics, proceed to Phase 3."
            },
            {
                "phase": "Phase 3 (Days 81 - 130)",
                "title": "Deep Learning & Generative AI",
                "focus": "Master neural networks with PyTorch/TensorFlow, Transformer architectures, Fine-Tuning LLMs, and RAG pipelines.",
                "action": "Build and deploy an AI-powered application."
            }
        ]
    },
    "database": {
        "title": "Database Engineering & Administration",
        "subdomains": {
            "db_management": {"roles": ["Database Administrator", "Database Engineer", "Database Developer", "SQL Developer", "Database Architect"], "skills": ["sql", "mysql", "postgresql", "mongodb", "query optimization", "pl/sql"]}
        },
        "core_skills": ["sql", "mysql", "postgresql", "mongodb", "indexing", "performance tuning", "pl/sql"],
        "certifications": ["Oracle Database Administrator Certified Professional", "MongoDB Certified Developer"],
        "roadmap": [
            {
                "phase": "Phase 1 (Days 1 - 30)",
                "title": "Relational Database Design & SQL",
                "focus": "Learn database normalization (1NF to 3NF), ER diagram modeling, advanced SQL queries, and stored procedures.",
                "action": "Once schema design is perfected, move to Phase 2."
            },
            {
                "phase": "Phase 2 (Days 31 - 70)",
                "title": "NoSQL Databases & Administration",
                "focus": "Master MongoDB document databases, CRUD operations, replication, and backup/recovery procedures.",
                "action": "After handling database scaling, proceed to Phase 3."
            },
            {
                "phase": "Phase 3 (Days 71 - 100)",
                "title": "Performance Tuning & Security",
                "focus": "Optimize query execution plans, indexing strategies, partitioning, and role-based access control.",
                "action": "Certify your database administration skills."
            }
        ]
    },
    "qa_testing": {
        "title": "QA & Software Testing",
        "subdomains": {
            "quality_assurance": {"roles": ["QA Engineer", "Software Test Engineer", "QA Analyst", "Automation Test Engineer", "Performance Test Engineer", "Manual Tester", "SDET"], "skills": ["selenium", "pytest", "postman", "automation testing", "manual testing", "java", "python"]}
        },
        "core_skills": ["selenium", "pytest", "postman", "automation", "manual testing", "java", "python", "sql"],
        "certifications": ["ISTQB Certified Tester", "Agile Tester Certification"],
        "roadmap": [
            {
                "phase": "Phase 1 (Days 1 - 30)",
                "title": "Manual Testing & SDLC",
                "focus": "Learn Software Development Life Cycle, test case writing, bug lifecycle management in Jira, and Agile ceremonies.",
                "action": "Once test plans are thorough, move to Phase 2."
            },
            {
                "phase": "Phase 2 (Days 31 - 70)",
                "title": "API & UI Test Automation",
                "focus": "Master REST API testing using Postman and UI test automation frameworks using Selenium with Python/Java.",
                "action": "After building automated test scripts, proceed to Phase 3."
            },
            {
                "phase": "Phase 3 (Days 71 - 100)",
                "title": "Performance Testing & SDET",
                "focus": "Learn load testing with JMeter and build robust test automation architectures (SDET).",
                "action": "Earn ISTQB certification and apply for QA roles."
            }
        ]
    },
    "system_admin": {
        "title": "System Administration & Linux/Windows",
        "subdomains": {
            "sys_admin": {"roles": ["System Administrator", "Linux Administrator", "Windows Administrator", "Systems Engineer", "Infrastructure Administrator"], "skills": ["linux", "bash", "active directory", "windows server", "networking", "virtualization"]}
        },
        "core_skills": ["linux", "bash scripting", "active directory", "windows server", "ssh", "virtualization", "vmware"],
        "certifications": ["RHCE (Red Hat Certified Engineer)", "Microsoft Certified: Windows Server Administrator"],
        "roadmap": [
            {
                "phase": "Phase 1 (Days 1 - 30)",
                "title": "Linux OS Administration",
                "focus": "Master terminal operations, user/group management, file permission models, cron jobs, and service daemons.",
                "action": "Once Linux servers are fully managed, move to Phase 2."
            },
            {
                "phase": "Phase 2 (Days 31 - 70)",
                "title": "Windows Server & Active Directory",
                "focus": "Configure Windows Server, Active Directory Domain Services (AD DS), Group Policies, DNS, and DHCP.",
                "action": "After setting up enterprise domain environments, proceed to Phase 3."
            },
            {
                "phase": "Phase 3 (Days 71 - 100)",
                "title": "Virtualization & Automation",
                "focus": "Deploy and manage VMware ESXi, Hyper-V, and automate administrative tasks using Shell/PowerShell scripts.",
                "action": "Prepare for Red Hat or Microsoft certifications."
            }
        ]
    },
    "it_support": {
        "title": "IT Support & Technical Operations",
        "subdomains": {
            "support_ops": {"roles": ["IT Support Engineer", "Technical Support Engineer", "Help Desk Technician", "IT Operations Analyst", "IT Operations Engineer", "Desktop Support Engineer"], "skills": ["troubleshooting", "active directory", "ticketing system", "hardware", "networking", "customer service"]}
        },
        "core_skills": ["troubleshooting", "active directory", "ticketing", "hardware", "os installation", "networking"],
        "certifications": ["CompTIA A+", "ITIL Foundation"],
        "roadmap": [
            {
                "phase": "Phase 1 (Days 1 - 25)",
                "title": "Hardware Diagnostics & OS Setup",
                "focus": "Learn PC hardware components, BIOS settings, clean Windows/Linux installation, and peripheral troubleshooting.",
                "action": "Once hardware repair workflows are clear, move to Phase 2."
            },
            {
                "phase": "Phase 2 (Days 26 - 55)",
                "title": "Helpdesk Ticketing & Networking",
                "focus": "Master IT support ticketing systems (ServiceNow/Jira), printer sharing, TCP/IP setup, and Wi-Fi troubleshooting.",
                "action": "After resolving simulated helpdesk tickets, proceed to Phase 3."
            },
            {
                "phase": "Phase 3 (Days 56 - 80)",
                "title": "ITIL Framework & Remote Support",
                "focus": "Understand ITIL service management frameworks, remote desktop tools, and corporate security guidelines.",
                "action": "Earn CompTIA A+ and ITIL certifications."
            }
        ]
    },
    "enterprise_tech": {
        "title": "Enterprise Technology (SAP, Salesforce, ERP)",
        "subdomains": {
            "erp_crm": {"roles": ["SAP Consultant", "ERP Consultant", "Salesforce Developer", "Salesforce Administrator", "CRM Consultant", "Enterprise Application Engineer"], "skills": ["sap abap", "salesforce", "apex", "crm", "erp", "sql"]}
        },
        "core_skills": ["salesforce", "apex", "sap abap", "erp", "crm", "sql", "integration"],
        "certifications": ["Salesforce Certified Platform Developer", "SAP Certified Development Associate"],
        "roadmap": [
            {
                "phase": "Phase 1 (Days 1 - 30)",
                "title": "CRM/ERP Architecture Basics",
                "focus": "Understand enterprise business workflows, CRM data models, and relational database structures.",
                "action": "Once data objects and relationships are clear, move to Phase 2."
            },
            {
                "phase": "Phase 2 (Days 31 - 70)",
                "title": "Customization & Development",
                "focus": "Learn Salesforce Apex programming, Lightning Web Components, or SAP ABAP module development.",
                "action": "After building custom enterprise applications, proceed to Phase 3."
            },
            {
                "phase": "Phase 3 (Days 71 - 100)",
                "title": "Integration & Security Administration",
                "focus": "Configure user profiles, permission sets, REST/SOAP API integrations, and workflow automation.",
                "action": "Take official Salesforce or SAP certification exams."
            }
        ]
    },
    "architecture": {
        "title": "Solution & Enterprise Architecture",
        "subdomains": {
            "system_arch": {"roles": ["Solutions Architect", "Technical Architect", "Enterprise Architect", "Cloud Architect", "Security Architect", "Software Architect"], "skills": ["system design", "microservices", "cloud architecture", "scalability", "enterprise security"]}
        },
        "core_skills": ["system design", "microservices", "cloud architecture", "scalability", "design patterns", "security"],
        "certifications": ["AWS Certified Solutions Architect – Professional", "TOGAF 9 Certified"],
        "roadmap": [
            {
                "phase": "Phase 1 (Days 1 - 30)",
                "title": "Design Principles & Patterns",
                "focus": "Master SOLID principles, object-oriented design patterns, and foundational system design concepts.",
                "action": "Once design patterns are understood, move to Phase 2."
            },
            {
                "phase": "Phase 2 (Days 31 - 70)",
                "title": "Distributed Systems & Scalability",
                "focus": "Learn load balancing, caching strategies (Redis), message queues (Kafka/RabbitMQ), and microservices communication.",
                "action": "After designing distributed systems, proceed to Phase 3."
            },
            {
                "phase": "Phase 3 (Days 71 - 110)",
                "title": "Cloud Architecture & Enterprise Security",
                "focus": "Design fault-tolerant, high-availability multi-cloud enterprise solutions with robust security compliance.",
                "action": "Prepare for TOGAF or AWS Professional Architect certifications."
            }
        ]
    },
    "business_analysis": {
        "title": "Business & Systems Analysis",
        "subdomains": {
            "biz_analysis": {"roles": ["Business Analyst", "IT Business Analyst", "Systems Analyst", "Business Systems Analyst", "Requirements Analyst"], "skills": ["requirement gathering", "uml", "sql", "agile", "wireframing", "excel"]}
        },
        "core_skills": ["requirements gathering", "sql", "agile", "jira", "excel", "process mapping", "uml"],
        "certifications": ["CBAP (Certified Business Analysis Professional)", "PMI-PBA"],
        "roadmap": [
            {
                "phase": "Phase 1 (Days 1 - 30)",
                "title": "Requirements Gathering & Documentation",
                "focus": "Learn stakeholder interviewing techniques, Business Requirements Documents (BRD), and Functional Specs (FRD).",
                "action": "Once documentation skills are sharp, move to Phase 2."
            },
            {
                "phase": "Phase 2 (Days 31 - 60)",
                "title": "Agile Methodologies & Tools",
                "focus": "Master Agile/Scrum frameworks, user story creation, acceptance criteria, and backlog management in Jira.",
                "action": "After managing sprints in simulations, proceed to Phase 3."
            },
            {
                "phase": "Phase 3 (Days 61 - 90)",
                "title": "Process Modeling & SQL Basics",
                "focus": "Learn UML diagrams, process flow mapping (BPMN), and basic SQL for data-driven business decisions.",
                "action": "Earn CBAP or business analysis certifications."
            }
        ]
    },
    "it_audit_risk": {
        "title": "IT Audit, Risk & Compliance (GRC)",
        "subdomains": {
            "grc_audit": {"roles": ["IT Auditor", "Information Systems Auditor", "Technology Risk Analyst", "GRC Analyst", "Compliance Analyst", "Security Auditor", "Risk Analyst"], "skills": ["iso 27001", "gdpr", "nist", "risk assessment", "audit", "compliance"]}
        },
        "core_skills": ["iso 27001", "nist", "risk assessment", "compliance", "auditing", "gdpr", "cybersecurity frameworks"],
        "certifications": ["CISA", "CRISC", "ISO 27001 Lead Auditor"],
        "roadmap": [
            {
                "phase": "Phase 1 (Days 1 - 30)",
                "title": "Frameworks & Compliance Standards",
                "focus": "Study ISO/IEC 27001, NIST Cybersecurity Framework, GDPR data protection, and HIPAA regulations.",
                "action": "Once framework controls are understood, move to Phase 2."
            },
            {
                "phase": "Phase 2 (Days 31 - 65)",
                "title": "Risk Assessment Methodologies",
                "focus": "Learn qualitative and quantitative risk analysis, threat modeling, and asset vulnerability mapping.",
                "action": "After evaluating risk registers, proceed to Phase 3."
            },
            {
                "phase": "Phase 3 (Days 66 - 100)",
                "title": "IT General Controls (ITGC) & Auditing",
                "focus": "Perform IT audits, test security controls, and write comprehensive compliance audit reports.",
                "action": "Prepare for CISA or CRISC certifications."
            }
        ]
    },
    "blockchain_web3": {
        "title": "Blockchain & Web3 Engineering",
        "subdomains": {
            "web3": {"roles": ["Blockchain Developer", "Blockchain Engineer", "Smart Contract Developer", "Web3 Developer", "Blockchain Security Engineer"], "skills": ["solidity", "smart contracts", "ethereum", "web3.js", "rust", "cryptography"]}
        },
        "core_skills": ["solidity", "smart contracts", "ethereum", "web3.js", "rust", "cryptography", "hardhat"],
        "certifications": ["Certified Blockchain Developer", "Consensys Developer Program"],
        "roadmap": [
            {
                "phase": "Phase 1 (Days 1 - 30)",
                "title": "Cryptography & Blockchain Basics",
                "focus": "Understand decentralized consensus mechanisms, cryptographic hashing, public-key cryptography, and EVM architecture.",
                "action": "Once underlying network mechanics are clear, move to Phase 2."
            },
            {
                "phase": "Phase 2 (Days 31 - 70)",
                "title": "Smart Contract Development",
                "focus": "Learn Solidity or Rust programming, write secure smart contracts, and test using Hardhat and Foundry.",
                "action": "After deploying contracts to testnets, proceed to Phase 3."
            },
            {
                "phase": "Phase 3 (Days 71 - 100)",
                "title": "Web3 Frontend & Smart Contract Auditing",
                "focus": "Build decentralized frontends using Ethers.js/Web3.js and audit smart contracts for reentrancy and overflow bugs.",
                "action": "Launch your Web3 project live."
            }
        ]
    },
    "iot_embedded": {
        "title": "IoT & Embedded Systems",
        "subdomains": {
            "embedded": {"roles": ["IoT Engineer", "IoT Developer", "IoT Security Engineer", "Embedded Engineer", "Firmware Engineer", "Embedded Software Developer"], "skills": ["embedded c", "microcontrollers", "arduino", "raspberry pi", "mqtt", "pcb design", "rtos"]}
        },
        "core_skills": ["embedded c", "microcontrollers", "iot", "mqtt", "pcb design", "arduino", "raspberry pi"],
        "certifications": ["ARM Accredited Engineer", "Embedded Systems Specialist"],
        "roadmap": [
            {
                "phase": "Phase 1 (Days 1 - 30)",
                "title": "Circuit & PCB Design Basics",
                "focus": "Learn schematic design, component selection, and PCB layout using KiCad or Altium Designer.",
                "action": "Once circuit design basics are mastered, move to Phase 2."
            },
            {
                "phase": "Phase 2 (Days 31 - 70)",
                "title": "Microcontrollers & Embedded C",
                "focus": "Master Embedded C programming, GPIO configuration, timers, and interrupts for microcontrollers (ESP32/AVR).",
                "action": "After writing hardware drivers, proceed to Phase 3."
            },
            {
                "phase": "Phase 3 (Days 71 - 100)",
                "title": "IoT Protocols & RTOS",
                "focus": "Implement communication protocols (SPI, I2C, UART, MQTT, HTTP) and Real-Time Operating Systems.",
                "action": "Build and showcase your custom IoT hardware prototype."
            }
        ]
    },
    "research_rd": {
        "title": "R&D & Security Research",
        "subdomains": {
            "research": {"roles": ["Research Engineer", "R&D Engineer", "Technology Researcher", "Research Scientist", "Security Researcher", "AI Researcher"], "skills": ["python", "research methodology", "paper writing", "reverse engineering", "experimentation"]}
        },
        "core_skills": ["python", "reverse engineering", "mathematics", "research methodology", "scientific writing", "analysis"],
        "certifications": ["Offensive Security Researcher Credentials", "Published IEEE/ACM Papers"],
        "roadmap": [
            {
                "phase": "Phase 1 (Days 1 - 30)",
                "title": "Literature Review & Research Methodology",
                "focus": "Learn how to read peer-reviewed journals, formulate research hypotheses, and design controlled experiments.",
                "action": "Once research scope is defined, move to Phase 2."
            },
            {
                "phase": "Phase 2 (Days 31 - 70)",
                "title": "Experimental Prototyping & Reverse Engineering",
                "focus": "Develop custom tools, proof-of-concept scripts in Python/C++, or analyze binary code via reverse engineering.",
                "action": "After gathering experimental data, proceed to Phase 3."
            },
            {
                "phase": "Phase 3 (Days 71 - 110)",
                "title": "Technical Whitepapers & Disclosure",
                "focus": "Write academic research papers, technical whitepapers, or responsible vulnerability disclosure reports.",
                "action": "Publish your findings or submit to conferences."
            }
        ]
    },
    "product_project_mgmt": {
        "title": "Product & Project Management",
        "subdomains": {
            "management": {"roles": ["Technical Product Manager", "Product Manager", "Product Analyst", "Product Owner", "IT Project Manager", "Technical Project Manager", "Program Manager"], "skills": ["agile", "scrum", "product roadmap", "jira", "stakeholder management", "sql"]}
        },
        "core_skills": ["agile", "scrum", "roadmap planning", "jira", "confluence", "product strategy", "sql"],
        "certifications": ["PMP (Project Management Professional)", "CSPO (Certified Scrum Product Owner)"],
        "roadmap": [
            {
                "phase": "Phase 1 (Days 1 - 30)",
                "title": "Agile & Scrum Frameworks",
                "focus": "Master sprint planning, backlog grooming, daily standups, and stakeholder management frameworks.",
                "action": "Once sprint execution workflows are clear, move to Phase 2."
            },
            {
                "phase": "Phase 2 (Days 31 - 65)",
                "title": "Product Strategy & Roadmapping",
                "focus": "Learn user persona research, MVP definition, product metrics (KPIs/OKRs), and feature prioritization.",
                "action": "After drafting comprehensive product roadmaps, proceed to Phase 3."
            },
            {
                "phase": "Phase 3 (Days 66 - 90)",
                "title": "Execution & Leadership",
                "focus": "Manage cross-functional engineering teams, release cycles, and enterprise risk management.",
                "action": "Prepare for PMP or CSPO certification exams."
            }
        ]
    },
    "it_consulting": {
        "title": "IT Consulting & Solutions",
        "subdomains": {
            "consulting": {"roles": ["IT Consultant", "Technology Consultant", "Cybersecurity Consultant", "Cloud Consultant", "Solutions Consultant"], "skills": ["client management", "solution presentation", "technical scoping", "enterprise strategy"]}
        },
        "core_skills": ["client communication", "solution design", "technical scoping", "presentation", "strategy"],
        "certifications": ["TOGAF", "AWS Certified Cloud Practitioner"],
        "roadmap": [
            {
                "phase": "Phase 1 (Days 1 - 25)",
                "title": "Client Discovery & Technical Scoping",
                "focus": "Learn effective client communication, business discovery workshops, and proposal writing.",
                "action": "Once scoping techniques are mastered, move to Phase 2."
            },
            {
                "phase": "Phase 2 (Days 26 - 60)",
                "title": "Solution Architecture & Presentation",
                "focus": "Design enterprise technical solutions and present high-impact business cases to stakeholders.",
                "action": "After practicing pitch decks and architecture reviews, proceed to Phase 3."
            },
            {
                "phase": "Phase 3 (Days 61 - 90)",
                "title": "Digital Transformation Advisory",
                "focus": "Guide enterprise migration, cloud adoption, and security posture enhancement projects.",
                "action": "Earn consulting and architectural certifications."
            }
        ]
    },
    "technical_documentation": {
        "title": "Technical Documentation & Knowledge Management",
        "subdomains": {
            "docs": {"roles": ["Technical Writer", "Documentation Engineer", "API Documentation Specialist", "Knowledge Management Specialist"], "skills": ["markdown", "git", "api documentation", "technical writing", "confluence", "swagger"]}
        },
        "core_skills": ["technical writing", "markdown", "api docs", "swagger/openapi", "git", "confluence"],
        "certifications": ["Certified Professional Technical Communicator (CPTC)"],
        "roadmap": [
            {
                "phase": "Phase 1 (Days 1 - 25)",
                "title": "Technical Writing Fundamentals",
                "focus": "Master clear, concise technical communication, grammar standards, and user manual structures.",
                "action": "Once user documentation is polished, move to Phase 2."
            },
            {
                "phase": "Phase 2 (Days 26 - 55)",
                "title": "API Documentation & Tools",
                "focus": "Learn OpenAPI / Swagger specifications, Markdown syntax, Git version control, and static site generators.",
                "action": "After documenting complex REST APIs, proceed to Phase 3."
            },
            {
                "phase": "Phase 3 (Days 56 - 80)",
                "title": "Enterprise Knowledge Bases",
                "focus": "Design searchable developer portals and enterprise knowledge management systems in Confluence.",
                "action": "Earn CPTC professional certification."
            }
        ]
    }
}

HTML_DASHBOARD = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CareerGuard Enterprise | AI Career & Skill Intelligence Platform</title>
    <style>
        :root {
            --bg-base: #07090e;
            --bg-card: #0d121f;
            --border-color: #1e293b;
            --accent-cyan: #38bdf8;
            --accent-blue: #0284c7;
            --accent-glow: rgba(56, 189, 248, 0.15);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }

        * { box-sizing: border-box; }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: var(--bg-base);
            color: var(--text-main);
            margin: 0;
            padding: 40px 20px;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(56, 189, 248, 0.05) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(2, 132, 199, 0.05) 0%, transparent 40%);
            min-height: 100vh;
        }

        .container {
            max-width: 1050px;
            margin: 0 auto;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 45px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7);
            position: relative;
            overflow: hidden;
        }

        .container::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, #38bdf8, #818cf8, #38bdf8);
        }

        .header-section {
            text-align: center;
            margin-bottom: 35px;
        }

        h1 {
            color: var(--accent-cyan);
            font-size: 2.8rem;
            margin: 0 0 10px 0;
            font-weight: 800;
            letter-spacing: -0.5px;
            text-shadow: 0 0 25px rgba(56, 189, 248, 0.3);
        }

        .subtitle {
            color: var(--text-muted);
            font-size: 1.15rem;
            margin: 0;
            font-weight: 400;
        }

        .form-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 25px;
            margin-bottom: 30px;
        }

        .form-group {
            display: flex;
            flex-direction: column;
        }

        label {
            margin-bottom: 10px;
            font-weight: 600;
            color: #e2e8f0;
            font-size: 0.95rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        select, input[type="file"] {
            padding: 14px 16px;
            background: #090d16;
            border: 1px solid #2a374a;
            color: var(--text-main);
            border-radius: 10px;
            font-size: 1rem;
            transition: all 0.3s ease;
            outline: none;
        }

        select:hover, select:focus, input[type="file"]:hover {
            border-color: var(--accent-cyan);
            box-shadow: 0 0 15px var(--accent-glow);
        }

        input[type="file"]::file-selector-button {
            background: #1e293b;
            color: var(--accent-cyan);
            border: none;
            padding: 8px 14px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            margin-right: 15px;
            transition: 0.2s;
        }

        input[type="file"]::file-selector-button:hover {
            background: var(--accent-cyan);
            color: var(--bg-base);
        }

        button.submit-btn {
            background: linear-gradient(135deg, #38bdf8, #0284c7);
            color: #07090e;
            border: none;
            padding: 16px;
            font-size: 1.15rem;
            font-weight: 800;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 20px rgba(56, 189, 248, 0.4);
            letter-spacing: 0.5px;
            margin-top: 10px;
        }

        button.submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(56, 189, 248, 0.6);
            opacity: 0.95;
        }

        .results-section {
            margin-top: 40px;
            background: #090d16;
            padding: 35px;
            border-radius: 16px;
            border: 1px solid #1e293b;
            border-left: 5px solid var(--accent-cyan);
            box-shadow: inset 0 2px 10px rgba(0,0,0,0.5);
        }

        .results-section h2 {
            margin-top: 0;
            color: var(--accent-cyan);
            font-size: 1.8rem;
        }

        .score-badge {
            font-size: 2.2rem;
            font-weight: 900;
            color: var(--accent-cyan);
            background: #0d121f;
            padding: 15px 25px;
            border-radius: 12px;
            display: inline-block;
            margin: 15px 0 20px 0;
            border: 1px solid #1e293b;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }

        .info-text {
            color: var(--text-muted);
            font-size: 1rem;
            margin-bottom: 20px;
            background: #0d121f;
            padding: 12px 16px;
            border-radius: 8px;
            border: 1px solid #1e293b;
        }

        .section-title {
            color: #f1f5f9;
            font-size: 1.2rem;
            margin: 25px 0 12px 0;
            font-weight: 700;
        }

        .skills-container {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }

        .tag-found {
            background: rgba(6, 95, 70, 0.4);
            color: #6ee7b7;
            border: 1px solid rgba(110, 231, 183, 0.3);
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 600;
        }

        .tag-missing {
            background: rgba(127, 29, 29, 0.4);
            color: #fca5a5;
            border: 1px solid rgba(252, 165, 165, 0.3);
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 600;
        }

        .tag-cert {
            background: #111827;
            color: #fbbf24;
            border: 1px solid rgba(251, 191, 36, 0.3);
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 600;
        }

        .roadmap-box {
            margin-top: 30px;
            background: #0d121f;
            padding: 25px;
            border-radius: 12px;
            border: 1px solid #1e293b;
        }

        .roadmap-step {
            margin-bottom: 22px;
            padding-left: 18px;
            border-left: 3px solid var(--accent-cyan);
        }

        .roadmap-step span.phase-tag {
            color: var(--accent-cyan);
            font-weight: 800;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .roadmap-step h4 {
            margin: 4px 0 6px 0;
            color: #f1f5f9;
            font-size: 1.15rem;
        }

        .roadmap-step p {
            margin: 0 0 6px 0;
            color: var(--text-muted);
            font-size: 0.95rem;
            line-height: 1.5;
        }

        .roadmap-step .action-guide {
            color: #38bdf8;
            font-size: 0.9rem;
            font-style: italic;
            font-weight: 600;
        }

        /* Creator Card Styles */
        .creator-card {
            margin-top: 45px;
            background: linear-gradient(135deg, #0d121f, #111827);
            border: 1px solid #22304a;
            padding: 30px;
            border-radius: 16px;
            border-top: 4px solid var(--accent-cyan);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }

        .creator-card h3 {
            margin-top: 0;
            color: var(--accent-cyan);
            font-size: 1.4rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .creator-card p {
            color: #cbd5e1;
            line-height: 1.7;
            font-size: 0.98rem;
            margin: 10px 0;
        }

        .creator-links {
            display: flex;
            gap: 15px;
            margin-top: 20px;
            flex-wrap: wrap;
        }

        .creator-links a {
            background: #090d16;
            border: 1px solid #334155;
            color: var(--accent-cyan);
            padding: 10px 18px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.92rem;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .creator-links a:hover {
            background: var(--accent-cyan);
            color: #07090e;
            border-color: var(--accent-cyan);
            box-shadow: 0 0 15px var(--accent-glow);
            transform: translateY(-2px);
        }

        .footer {
            text-align: center;
            margin-top: 40px;
            font-size: 0.9rem;
            color: #64748b;
            border-top: 1px solid #1e293b;
            padding-top: 20px;
        }

        .footer span {
            color: var(--accent-cyan);
            font-weight: 700;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header-section">
            <h1>CareerGuard 🛡️</h1>
            <div class="subtitle">Enterprise-Grade Multi-Domain AI Career Intelligence & ATS Optimizer</div>
        </div>
        
        <form method="POST" enctype="multipart/form-data" class="form-grid">
            <div class="form-group">
                <label> Select Target Industry Domain / Engineering Branch:</label>
                <select name="domain" required>
                    {% for key, val in domains.items() %}
                        <option value="{{ key }}" {% if selected_domain == key %}selected{% endif %}>{{ val.title }}</option>
                    {% endfor %}
                </select>
            </div>
            
            <div class="form-group">
                <label> Upload Professional Resume (PDF):</label>
                <input type="file" name="resume" accept=".pdf" required>
            </div>
            
            <button type="submit" class="submit-btn">Run Live ATS & Sequential Skill-Gap Analysis </button>
        </form>

        {% if result %}
        <div class="results-section">
            <h2>Analysis Report: {{ role_title }}</h2>
            <div class="score-badge">Live ATS Compatibility Score: {{ ats_score }}%</div>
            
            <div class="info-text"><b>Extracted Contact / Candidate Info:</b> {{ contact_info }}</div>
            
            <div class="section-title">✅ Matched Industry Core Skills Found:</div>
            <div class="skills-container">
                {% for skill in found_skills %}
                    <span class="tag-found">{{ skill }}</span>
                {% endfor %}
                {% if not found_skills %}<span>No core skills detected in resume text.</span>{% endif %}
            </div>

            <div class="section-title">⚠️ Missing Skills & Gaps:</div>
            <div class="skills-container">
                {% for skill in missing_skills %}
                    <span class="tag-missing">{{ skill }}</span>
                {% endfor %}
                {% if not missing_skills %}<span>Zero skill gaps! Excellent profile match.</span>{% endif %}
            </div>

            <div class="section-title">🏆 Recommended Industry Certifications Missing:</div>
            <div class="skills-container">
                {% for cert in missing_certs %}
                    <span class="tag-cert">🔒 {{ cert }}</span>
                {% endfor %}
            </div>

            <div class="roadmap-box">
                <h3 style="margin-top: 0; color: var(--accent-cyan);">📈 Sequential Beginner-to-Advanced Mastery Roadmap:</h3>
                <p style="color: var(--text-muted); margin-bottom: 20px; font-size: 0.95rem;">Follow this structured progression sequentially. Complete Phase 1 fully before moving to Phase 2, and so on:</p>
                {% for item in roadmap %}
                    <div class="roadmap-step">
                        <span class="phase-tag">{{ item.phase }}</span>
                        <h4>{{ item.title }}</h4>
                        <p>{{ item.focus }}</p>
                        <div class="action-guide">👉 Next Step: {{ item.action }}</div>
                    </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}

        <!-- About the Creator Section -->
        <div class="creator-card">
            <h3>👨‍💻 About the Creator</h3>
            <p><b>Saud Nadaf</b><br>
            B.Tech CSE — Cyber Security | Darbhanga College of Engineering<br>
            Cybersecurity-focused student working across VAPT, web and application security, digital forensics, vulnerability research and security automation. Focused on building practical security projects, exploring real-world security problems, and continuously developing advanced technical solutions.</p>
            
            <p style="margin-bottom: 6px;"><b>Technical Focus:</b> VAPT · Web Security · Application Security · Digital Forensics · Security Research · SOC/Blue Team · Security Automation</p>
            <p style="margin-top: 0; margin-bottom: 15px;"><b>Selected Work:</b> VAULTX · SecTrace · Research & R&D Projects</p>

            <div class="creator-links">
                <a href="https://github.com/saudnadaf09" target="_blank">
                    🔗 GitHub Profile
                </a>
                <a href="https://www.linkedin.com/in/saud-nadaf-41b015343/" target="_blank">
                    💼 LinkedIn Profile
                </a>
                <a href="mailto:saudnadaf.infosec@proton.me">
                    ✉️ Email: saudnadaf.infosec@proton.me
                </a>
            </div>
        </div>

        <div class="footer">
            Developed with mastery and precision by <span>Saud Nadaf</span>  | Enterprise Career Intelligence Ecosystem
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = False
    found_skills = []
    missing_skills = []
    missing_certs = []
    ats_score = 0
    role_title = ""
    roadmap = []
    contact_info = "Not Detected"
    selected_domain = "cybersecurity"

    if request.method == 'POST':
        selected_domain = request.form.get('domain', 'cybersecurity')
        file = request.files.get('resume')
        
        if file and file.filename.endswith('.pdf'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            
            extracted_text = ""
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        extracted_text += text + "\n"
            
            lower_text = extracted_text.lower()
            
            emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', extracted_text)
            phones = re.findall(r'\+?\d[\d -]{8,12}\d', extracted_text)
            email_str = emails[0] if emails else "Email Hidden/Not Found"
            phone_str = phones[0] if phones else "Phone Hidden/Not Found"
            contact_info = f"Email: {email_str} | Phone: {phone_str}"

            domain_data = DOMAIN_TAXONOMY.get(selected_domain, DOMAIN_TAXONOMY['cybersecurity'])
            role_title = domain_data['title']
            required_skills = domain_data['core_skills']
            all_certs = domain_data['certifications']
            roadmap = domain_data['roadmap']
            
            for skill in required_skills:
                if skill in lower_text:
                    found_skills.append(skill.title())
                else:
                    missing_skills.append(skill.title())
            
            for cert in all_certs:
                if cert.lower() not in lower_text:
                    missing_certs.append(cert)
            
            total = len(required_skills)
            found_count = len(found_skills)
            ats_score = int((found_count / total) * 100) if total > 0 else 0
            result = True

    return render_template_string(
        HTML_DASHBOARD,
        domains=DOMAIN_TAXONOMY,
        selected_domain=selected_domain,
        result=result, 
        role_title=role_title, 
        ats_score=ats_score, 
        found_skills=found_skills, 
        missing_skills=missing_skills, 
        missing_certs=missing_certs,
        roadmap=roadmap,
        content_info=contact_info,
        contact_info=contact_info
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)