# Este archivo en concreto fue hecho con ayuda de claude para el enorme database necesario para la prediccion.
"""
predict.py  —  Advanced Hybrid CV Parser
=========================================
Hybrid system: ML model + weighted skill scoring + heuristics.
No transformers, no deep learning, no external APIs.
Pure scikit-learn + regex + NLP clásico.
"""

import pickle
import re
import unicodedata
import numpy as np
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

def normalize(text: str) -> str:
    """Full unicode normalization, lowercase, accent stripping, symbol clean."""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")
    text = text.lower()
    # preserve: letters, digits, + # . - / (for c++, c#, tcp/ip, node.js, ci/cd)
    text = re.sub(r"[^a-z0-9+#.\-/\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

_area_model      = None
_seniority_model = None
_area_labels: List[str] = []


def load_models(
    area_path:      str = "ai/model/saved/area_model.pkl",
    seniority_path: str = "ai/model/saved/seniority_model.pkl",
    labels_path:    str = "ai/model/saved/area_labels.pkl",
):
    global _area_model, _seniority_model, _area_labels

    with open(area_path, "rb") as f:
        _area_model = pickle.load(f)

    with open(seniority_path, "rb") as f:
        _seniority_model = pickle.load(f)

    try:
        with open(labels_path, "rb") as f:
            _area_labels = pickle.load(f)
    except FileNotFoundError:
        _area_labels = list(getattr(_area_model, "classes_", []))

    return _area_model, _seniority_model

# Alias creados con claude:

SKILL_ALIASES: Dict[str, List[str]] = {

    "Python":       ["python"],
    "Java":         ["java"],
    "JavaScript":   ["javascript"],
    "TypeScript":   ["typescript"],
    "PHP":          ["php"],
    "Ruby":         ["ruby"],
    "Scala":        ["scala"],
    "Kotlin":       ["kotlin"],
    "Rust":         ["rust"],
    "Elixir":       ["elixir"],

    # ─── Backend frameworks ───────────────────────────────

    "Node.js":      ["node.js", "nodejs", "node js"],
    "Express":      ["express", "expressjs", "express.js"],
    "Django":       ["django"],
    "FastAPI":      ["fastapi", "fast api"],
    "Flask":        ["flask"],
    "Spring Boot":  ["spring boot", "spring-boot"],
    "Spring":       ["spring"],
    "Laravel":      ["laravel"],
    "Symfony":      ["symfony"],
    "Rails":        ["ruby on rails", "rails"],
    "ASP.NET":      ["asp.net", "aspnet"],
    ".NET":         [".net", "dotnet", "dot net"],
    "NestJS":       ["nestjs", "nest.js"],
    "FastAPI":      ["fastapi"],
    "Gin":          ["gin framework", "gin golang"],
    "Fiber":        ["fiber golang"],
    "Actix":        ["actix"],

    # ─── API / protocols ─────────────────────────────────
    "REST API":     ["rest api", "restful api", "api rest", "restful", "rest"],
    "GraphQL":      ["graphql"],
    "gRPC":         ["grpc"],
    "WebSockets":   ["websocket", "websockets"],
    "JWT":          ["jwt"],
    "OAuth2":       ["oauth2", "oauth"],
    "OpenAPI":      ["openapi", "swagger"],

    # ─── Frontend frameworks ─────────────────────────────
    "React":        ["react", "reactjs", "react.js"],
    "Angular":      ["angular"],
    "Vue.js":       ["vue.js", "vuejs", "vue"],
    "Svelte":       ["svelte"],
    "Next.js":      ["next.js", "nextjs"],
    "Nuxt.js":      ["nuxt.js", "nuxtjs"],
    "Astro":        ["astro"],
    "HTML5":        ["html5", "html"],
    "CSS3":         ["css3", "css"],
    "TailwindCSS":  ["tailwindcss", "tailwind"],
    "Bootstrap":    ["bootstrap"],
    "SASS/SCSS":    ["sass", "scss"],
    "Redux":        ["redux"],
    "Vuex":         ["vuex"],
    "Webpack":      ["webpack"],
    "Vite":         ["vite"],
    "Babel":        ["babel"],

    # ─── Mobile ───────────────────────────────────────────
    "Flutter":      ["flutter"],
    "Dart":         ["dart"],
    "Swift":        ["swift"],
    "React Native": ["react native"],
    "Expo":         ["expo"],
    "Android":      ["android"],
    "iOS":          ["ios"],
    "Jetpack Compose": ["jetpack compose"],
    "SwiftUI":      ["swiftui"],
    "UIKit":        ["uikit"],
    "Core Data":    ["core data"],
    "Hilt":         ["hilt"],
    "Coroutines":   ["coroutines"],
    "MVVM":         ["mvvm"],
    "Retrofit":     ["retrofit"],

    # ─── Databases ────────────────────────────────────────
    "PostgreSQL":   ["postgresql", "postgres", "psql"],
    "MySQL":        ["mysql"],
    "MariaDB":      ["mariadb"],
    "MongoDB":      ["mongodb", "mongo"],
    "Redis":        ["redis"],
    "SQLite":       ["sqlite"],
    "Oracle DB":    ["oracle db", "oracle database"],
    "SQL Server":   ["sql server", "sqlserver", "mssql"],
    "DynamoDB":     ["dynamodb"],
    "Elasticsearch": ["elasticsearch", "elastic search"],
    "Cassandra":    ["cassandra"],
    "CouchDB":      ["couchdb"],
    "InfluxDB":     ["influxdb"],
    "Neo4j":        ["neo4j"],
    "Snowflake":    ["snowflake"],
    "BigQuery":     ["bigquery"],
    "Redshift":     ["redshift"],
    "SQLAlchemy":   ["sqlalchemy"],
    "Prisma":       ["prisma"],
    "NoSQL":        ["nosql"],
    "ETL":          ["etl"],
    "Data Warehouse": ["data warehouse", "datawarehouse"],

    # ─── Messaging / async ───────────────────────────────
    "Apache Kafka": ["apache kafka", "kafka"],
    "RabbitMQ":     ["rabbitmq", "rabbit mq"],
    "Celery":       ["celery"],
    "Sidekiq":      ["sidekiq"],
    "Bull":         ["bull queue", "bullmq"],
    "Apache Spark": ["apache spark", "spark"],
    "Apache Airflow": ["apache airflow", "airflow"],

    # ─── DevOps / Infra ───────────────────────────────────
    "Docker":       ["docker"],
    "Kubernetes":   ["kubernetes", "k8s"],
    "Terraform":    ["terraform"],
    "Ansible":      ["ansible"],
    "Helm":         ["helm"],
    "ArgoCD":       ["argocd"],
    "GitOps":       ["gitops"],
    "Jenkins":      ["jenkins"],
    "GitHub Actions": ["github actions"],
    "GitLab CI":    ["gitlab ci", "gitlab-ci"],
    "CircleCI":     ["circleci"],
    "Travis CI":    ["travis ci"],
    "CI/CD":        ["ci/cd", "cicd", "continuous integration", "continuous delivery"],
    "Nginx":        ["nginx"],
    "Apache":       ["apache httpd", "apache server"],
    "HAProxy":      ["haproxy"],
    "Vault":        ["hashicorp vault", "vault secrets"],
    "Consul":       ["consul"],
    "Prometheus":   ["prometheus"],
    "Grafana":      ["grafana"],
    "Datadog":      ["datadog"],
    "ELK Stack":    ["elk stack", "elasticsearch kibana", "logstash"],
    "Zabbix":       ["zabbix"],
    "Nagios":       ["nagios"],
    "Vagrant":      ["vagrant"],
    "Packer":       ["packer"],
    "OPA":          ["open policy agent", "opa policy"],
    "Crossplane":   ["crossplane"],
    "Istio":        ["istio"],
    "Linux":        ["linux"],
    "Ubuntu":       ["ubuntu"],
    "Debian":       ["debian"],
    "CentOS":       ["centos"],
    "RHEL":         ["rhel", "red hat enterprise linux"],
    "Bash":         ["bash", "shell scripting", "bash scripting"],
    "SSH":          ["ssh"],
    "VPN":          ["vpn"],

    # ─── Cloud ────────────────────────────────────────────
    "AWS":          ["aws", "amazon web services"],
    "GCP":          ["gcp", "google cloud platform", "google cloud"],
    "Azure":        ["azure", "microsoft azure"],
    "AWS Lambda":   ["aws lambda", "lambda functions"],
    "EC2":          ["ec2"],
    "S3":           ["s3 bucket", "amazon s3"],
    "EKS":          ["eks"],
    "ECS":          ["ecs"],
    "CloudFormation": ["cloudformation"],
    "Pulumi":       ["pulumi"],
    "Serverless":   ["serverless"],
    "Cloud Run":    ["cloud run"],
    "Compute Engine": ["compute engine"],
    "Nutanix":      ["nutanix"],
    "VMware":       ["vmware", "vmware vsphere", "vsphere", "vcenter"],
    "Hyper-V":      ["hyper-v", "hyperv"],
    "KVM":          ["kvm hypervisor"],
    "Proxmox":      ["proxmox"],
    "VirtualBox":   ["virtualbox"],

    # ─── Networking ───────────────────────────────────────
    "CCNA":         ["ccna"],
    "CCNP":         ["ccnp"],
    "CCIE":         ["ccie"],
    "Cisco":        ["cisco"],
    "Mikrotik":     ["mikrotik"],
    "Juniper":      ["juniper"],
    "Palo Alto":    ["palo alto", "paloalto"],
    "Fortinet":     ["fortinet", "fortigate"],
    "Routing":      ["routing", "enrutamiento"],
    "Switching":    ["switching", "conmutacion"],
    "VLAN":         ["vlan", "vlans"],
    "BGP":          ["bgp"],
    "OSPF":         ["ospf"],
    "EIGRP":        ["eigrp"],
    "MPLS":         ["mpls"],
    "SD-WAN":       ["sd-wan", "sdwan"],
    "TCP/IP":       ["tcp/ip", "tcp ip", "tcpip"],
    "DNS":          ["dns"],
    "DHCP":         ["dhcp"],
    "NAT":          ["nat"],
    "Firewall":     ["firewall", "firewalls"],
    "VoIP":         ["voip"],
    "Wireshark":    ["wireshark"],
    "Network Monitoring": ["network monitoring", "monitoreo de red"],
    "QoS":          ["qos"],
    "Spanning Tree": ["spanning tree", "stp"],
    "802.1Q":       ["802.1q"],
    "RADIUS":       ["radius"],
    "TACACS":       ["tacacs"],
    "IDS/IPS":      ["ids/ips", "ids ips", "intrusion detection"],

    # ─── SysAdmin ─────────────────────────────────────────
    "Active Directory": ["active directory", "ad domain"],
    "Windows Server": ["windows server"],
    "Group Policy": ["group policy", "gpo"],
    "Exchange":     ["exchange server"],
    "Hyper-V":      ["hyper-v"],
    "PowerShell":   ["powershell"],
    "Samba":        ["samba"],
    "NFS":          ["nfs"],
    "LVM":          ["lvm"],
    "RAID":         ["raid"],
    "Backup":       ["backup", "respaldo"],
    "Fail2ban":     ["fail2ban"],
    "UFW":          ["ufw"],
    "iptables":     ["iptables"],
    "Cron":         ["cron", "crontab"],
    "Systemd":      ["systemd"],
    "Netplan":      ["netplan"],
    "PgBouncer":    ["pgbouncer"],
    "Patroni":      ["patroni"],
    "HAProxy":      ["haproxy"],

    # ─── Data Science / ML ───────────────────────────────
    "TensorFlow":   ["tensorflow"],
    "PyTorch":      ["pytorch"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "Pandas":       ["pandas"],
    "NumPy":        ["numpy"],
    "Keras":        ["keras"],
    "XGBoost":      ["xgboost"],
    "LightGBM":     ["lightgbm"],
    "Matplotlib":   ["matplotlib"],
    "Seaborn":      ["seaborn"],
    "Jupyter":      ["jupyter", "jupyter notebook"],
    "NLP":          ["nlp", "natural language processing"],
    "BERT":         ["bert"],
    "OpenCV":       ["opencv"],
    "Machine Learning": ["machine learning", "aprendizaje automatico"],
    "Deep Learning": ["deep learning", "aprendizaje profundo"],
    "Computer Vision": ["computer vision", "vision por computadora"],
    "dbt":          ["dbt"],
    "Hadoop":       ["hadoop"],

    # ─── QA / Testing ────────────────────────────────────
    "Selenium":     ["selenium"],
    "Cypress":      ["cypress"],
    "Playwright":   ["playwright"],
    "PyTest":       ["pytest"],
    "JUnit":        ["junit"],
    "RSpec":        ["rspec"],
    "PHPUnit":      ["phpunit"],
    "Appium":       ["appium"],
    "Postman":      ["postman"],
    "JMeter":       ["jmeter"],
    "Cucumber":     ["cucumber", "bdd"],
    "Testing":      ["testing", "qa testing", "software testing"],

    # ─── Security ────────────────────────────────────────
    "Ethical Hacking": ["ethical hacking", "hacking etico"],
    "Pentesting":   ["pentesting", "penetration testing", "pen testing"],
    "OWASP":        ["owasp"],
    "SIEM":         ["siem"],
    "SOC":          ["soc analyst", "security operations"],
    "Malware Analysis": ["malware analysis", "analisis malware"],
    "CEH":          ["ceh"],
    "OSCP":         ["oscp"],
    "Security+":    ["security+", "comptia security"],
    "Cybersecurity": ["cybersecurity", "ciberseguridad"],
    "Vulnerability Assessment": ["vulnerability assessment", "evaluacion de vulnerabilidades"],
    "Red Team":     ["red team"],
    "Blue Team":    ["blue team"],
    "Zero Trust":   ["zero trust", "zero-trust"],
    "NGFW":         ["ngfw", "next generation firewall"],
    "NAC":          ["nac"],

    # ─── Design / UX ─────────────────────────────────────
    "Figma":        ["figma"],
    "Sketch":       ["sketch"],
    "Adobe XD":     ["adobe xd"],
    "Photoshop":    ["photoshop"],
    "Illustrator":  ["illustrator"],
    "InDesign":     ["indesign"],
    "After Effects": ["after effects"],
    "Canva":        ["canva"],
    "UX Research":  ["ux research", "user research"],
    "Wireframes":   ["wireframe", "wireframes"],
    "Prototyping":  ["prototyping", "prototipado"],
    "Design System": ["design system"],
    "Motion Design": ["motion design"],

    # ─── Tools / General ─────────────────────────────────
    "Git":          ["git"],
    "GitHub":       ["github"],
    "GitLab":       ["gitlab"],
    "Bitbucket":    ["bitbucket"],
    "Jira":         ["jira"],
    "Confluence":   ["confluence"],
    "Slack":        ["slack api"],
    "Firebase":     ["firebase"],
    "Supabase":     ["supabase"],
    "WordPress":    ["wordpress"],
    "Strapi":       ["strapi"],

    # ─── Methodologies ───────────────────────────────────
    "Agile":        ["agile", "agile methodology"],
    "Scrum":        ["scrum"],
    "Kanban":       ["kanban"],
    "Microservices": ["microservices", "microservicios"],
    "Event-Driven": ["event-driven", "event driven architecture"],
    "TDD":          ["tdd", "test driven development"],
    "DDD":          ["ddd", "domain driven design"],
}

# ─── Context-gated ambiguous skills ──────────────────────
# These use look-ahead/look-behind or require surrounding tech context.
# Matched separately to avoid false positives in normal prose.

CONTEXT_SKILLS: List[Tuple[str, str]] = [
    # Go/Golang  — match "go" only when adjacent to known go ecosystem terms
    ("Go",   r"\b(?:go(?:lang)?|golang)\b"),
    # C++
    ("C++",  r"\bc\+\+\b"),
    # C#
    ("C#",   r"\bc#\b"),
    # R  — only when preceded/followed by data-science context words
    ("R",    r"(?:(?:ggplot|dplyr|tidyverse|shiny|rstudio|caret|r studio)\b|\bR\b(?=\s*(?:language|programming|studio|shiny|tidyverse|ggplot)))"),
    # SQL  — common word but valid tech skill
    ("SQL",  r"\bsql\b"),
]


# =========================================================
# CATEGORY → CANONICAL SKILLS MAPPING
# =========================================================

CATEGORY_SKILLS: Dict[str, List[str]] = {

    "Backend": [
        "Python", "Java", "JavaScript", "TypeScript", "PHP", "Ruby",
        "Scala", "Go", "C#", "Kotlin", "Rust", "Elixir",
        "Node.js", "Express", "Django", "FastAPI", "Flask",
        "Spring Boot", "Spring", "Laravel", "Symfony", "Rails",
        "ASP.NET", ".NET", "NestJS", "Gin", "Fiber", "Actix",
        "REST API", "GraphQL", "gRPC", "WebSockets",
        "JWT", "OAuth2", "OpenAPI",
        "Apache Kafka", "RabbitMQ", "Celery", "Sidekiq", "Bull",
        "SQLAlchemy", "Prisma",
    ],

    "Frontend": [
        "React", "Angular", "Vue.js", "Svelte", "Next.js", "Nuxt.js", "Astro",
        "HTML5", "CSS3", "TailwindCSS", "Bootstrap", "SASS/SCSS",
        "Redux", "Vuex", "Webpack", "Vite", "Babel",
        "JavaScript", "TypeScript",
    ],

    "Mobile": [
        "Flutter", "Dart", "Swift", "React Native", "Expo",
        "Android", "iOS", "Kotlin",
        "Jetpack Compose", "SwiftUI", "UIKit", "Core Data",
        "Hilt", "Coroutines", "MVVM", "Retrofit", "Firebase",
    ],

    "Database": [
        "PostgreSQL", "MySQL", "MariaDB", "MongoDB", "Redis",
        "SQLite", "Oracle DB", "SQL Server", "DynamoDB",
        "Elasticsearch", "Cassandra", "CouchDB", "InfluxDB",
        "Neo4j", "Snowflake", "BigQuery", "Redshift",
        "SQLAlchemy", "Prisma", "NoSQL", "ETL",
        "Data Warehouse", "SQL", "PgBouncer", "Patroni",
    ],

    "DevOps": [
        "Docker", "Kubernetes", "Terraform", "Ansible", "Helm",
        "ArgoCD", "GitOps", "Jenkins", "GitHub Actions", "GitLab CI",
        "CircleCI", "Travis CI", "CI/CD",
        "Nginx", "HAProxy", "Vault", "Consul",
        "Prometheus", "Grafana", "Datadog", "ELK Stack",
        "Linux", "Ubuntu", "Debian", "CentOS", "RHEL",
        "Bash", "SSH", "VPN",
        "Zabbix", "Nagios", "Vagrant", "Packer",
        "OPA", "Crossplane", "Istio",
    ],

    "Cloud Computing": [
        "AWS", "GCP", "Azure",
        "AWS Lambda", "EC2", "S3", "EKS", "ECS",
        "CloudFormation", "Pulumi", "Serverless",
        "Cloud Run", "Compute Engine", "BigQuery",
        "Terraform", "Ansible",
    ],

    "Networking": [
        "CCNA", "CCNP", "CCIE", "Cisco", "Mikrotik",
        "Juniper", "Palo Alto", "Fortinet",
        "Routing", "Switching", "VLAN",
        "BGP", "OSPF", "EIGRP", "MPLS", "SD-WAN",
        "TCP/IP", "DNS", "DHCP", "NAT",
        "Firewall", "VoIP", "Wireshark",
        "Network Monitoring", "QoS",
        "Spanning Tree", "802.1Q", "RADIUS", "TACACS",
        "IDS/IPS", "VPN",
    ],

    "SysAdmin": [
        "Linux", "Ubuntu", "Debian", "CentOS", "RHEL",
        "Windows Server", "Active Directory", "Group Policy",
        "Exchange", "Hyper-V", "PowerShell", "Bash",
        "VMware", "Nutanix", "KVM", "Proxmox", "VirtualBox",
        "Ansible", "Zabbix", "Nagios",
        "Samba", "NFS", "LVM", "RAID",
        "Backup", "Fail2ban", "UFW", "iptables",
        "Cron", "Systemd", "Netplan", "SSH",
    ],

    "Infraestructura": [
        "VMware", "Nutanix", "KVM", "Proxmox", "VirtualBox", "Hyper-V",
        "Cisco", "Routing", "Switching", "VLAN",
        "Firewall", "IDS/IPS",
        "Docker", "Kubernetes",
        "Linux", "Windows Server",
        "Backup", "RAID", "NFS",
        "Zabbix", "Nagios", "Grafana",
        "AWS", "Azure", "GCP",
    ],

    "Soporte Técnico": [
        "Windows Server", "Active Directory", "Group Policy",
        "Linux", "DNS", "DHCP",
        "Firewall", "VPN",
        "Backup", "PowerShell", "Bash",
        "Ticketing", "Helpdesk",
    ],

    "Data Science": [
        "Python", "R",
        "TensorFlow", "PyTorch", "scikit-learn",
        "Pandas", "NumPy", "Keras",
        "XGBoost", "LightGBM",
        "Matplotlib", "Seaborn", "Jupyter",
        "NLP", "BERT", "OpenCV",
        "Machine Learning", "Deep Learning", "Computer Vision",
        "dbt", "Hadoop", "Apache Spark", "Apache Airflow",
        "BigQuery", "Snowflake", "Redshift", "ETL",
        "SQL",
    ],

    "QA": [
        "Selenium", "Cypress", "Playwright", "PyTest",
        "JUnit", "RSpec", "PHPUnit",
        "Appium", "Postman", "JMeter",
        "Cucumber", "Testing",
    ],

    "Seguridad": [
        "Ethical Hacking", "Pentesting", "OWASP",
        "SIEM", "SOC", "Malware Analysis",
        "CEH", "OSCP", "Security+", "Cybersecurity",
        "Vulnerability Assessment", "Red Team", "Blue Team",
        "Zero Trust", "NGFW", "NAC",
        "Palo Alto", "Fortinet", "IDS/IPS",
        "Firewall",
    ],

    "Diseño": [
        "Figma", "Sketch", "Adobe XD",
        "Photoshop", "Illustrator", "InDesign",
        "After Effects", "Canva",
        "UX Research", "Wireframes", "Prototyping",
        "Design System", "Motion Design",
    ],

    "Fullstack": [
        "React", "Angular", "Vue.js", "Next.js",
        "Node.js", "Django", "Rails", "Laravel",
        "HTML5", "CSS3", "JavaScript", "TypeScript",
        "PostgreSQL", "MongoDB", "Redis",
        "Docker", "AWS", "GCP",
    ],
}


# =========================================================
# AREA WEIGHTS  —  higher = stronger signal for that area
# =========================================================

AREA_WEIGHTS: Dict[str, Dict[str, float]] = {

    "Backend": {
        "Node.js": 6, "Express": 5, "NestJS": 5,
        "Spring Boot": 6, "Spring": 4,
        "Django": 5, "FastAPI": 5, "Flask": 4,
        "Laravel": 5, "Rails": 5, "Symfony": 4,
        "ASP.NET": 5, ".NET": 4,
        "GraphQL": 4, "gRPC": 4,
        "REST API": 4, "JWT": 3, "OAuth2": 3,
        "Apache Kafka": 4, "RabbitMQ": 4, "Celery": 3,
        "Microservices": 4, "Event-Driven": 3,
        "Python": 2, "Java": 2, "PHP": 2, "Ruby": 2,
        "Go": 3, "Rust": 3,
    },

    "Frontend": {
        "React": 6, "Next.js": 6, "Angular": 5,
        "Vue.js": 5, "Nuxt.js": 5, "Svelte": 5,
        "TailwindCSS": 4, "Redux": 4, "Vuex": 4,
        "HTML5": 3, "CSS3": 3, "Vite": 3,
        "SASS/SCSS": 3, "Bootstrap": 2,
        "TypeScript": 3, "JavaScript": 2,
    },

    "Mobile": {
        "Flutter": 7, "React Native": 7,
        "Swift": 7, "SwiftUI": 7, "UIKit": 6,
        "Kotlin": 6, "Jetpack Compose": 6,
        "Android": 5, "iOS": 5, "Dart": 5,
        "Expo": 4, "Hilt": 4, "Coroutines": 4,
    },

    "Database": {
        "PostgreSQL": 4, "MySQL": 4, "MongoDB": 4,
        "Redis": 3, "Elasticsearch": 4,
        "SQL Server": 4, "Oracle DB": 4,
        "DynamoDB": 4, "Cassandra": 4,
        "Snowflake": 5, "BigQuery": 5, "Redshift": 5,
        "ETL": 4, "Data Warehouse": 5,
        "PgBouncer": 4, "Patroni": 4,
    },

    "DevOps": {
        "Docker": 6, "Kubernetes": 7, "Helm": 5,
        "Terraform": 6, "Ansible": 5,
        "ArgoCD": 6, "GitOps": 5,
        "Jenkins": 4, "GitHub Actions": 4,
        "CI/CD": 4, "GitLab CI": 4,
        "Linux": 4, "Bash": 3, "SSH": 3,
        "Nginx": 3, "Prometheus": 4, "Grafana": 4,
        "Datadog": 4, "ELK Stack": 4,
        "Istio": 5, "Crossplane": 5, "OPA": 4,
    },

    "Cloud Computing": {
        "AWS": 6, "GCP": 6, "Azure": 6,
        "AWS Lambda": 5, "EC2": 4, "S3": 4,
        "EKS": 5, "ECS": 4,
        "CloudFormation": 5, "Pulumi": 5,
        "Serverless": 4, "Terraform": 4,
        "Cloud Run": 5, "Compute Engine": 4,
    },

    "Networking": {
        "CCNA": 9, "CCNP": 10, "CCIE": 10,
        "Cisco": 7, "Mikrotik": 6,
        "Routing": 6, "Switching": 6, "VLAN": 6,
        "BGP": 7, "OSPF": 6, "EIGRP": 6,
        "MPLS": 7, "SD-WAN": 7,
        "TCP/IP": 4, "DNS": 3, "DHCP": 3,
        "Firewall": 4, "IDS/IPS": 4,
        "Wireshark": 4, "VoIP": 4,
        "Network Monitoring": 4, "QoS": 4,
        "Palo Alto": 5, "Fortinet": 5, "Juniper": 5,
    },

    "SysAdmin": {
        "Linux": 5, "Ubuntu": 4, "CentOS": 4, "RHEL": 4,
        "Windows Server": 6, "Active Directory": 7,
        "Group Policy": 5, "PowerShell": 5,
        "VMware": 6, "Hyper-V": 5, "Nutanix": 5,
        "KVM": 4, "Proxmox": 5,
        "Ansible": 4, "Zabbix": 5, "Nagios": 4,
        "Backup": 4, "RAID": 4, "iptables": 4,
        "Systemd": 3, "Bash": 3,
    },

    "Infraestructura": {
        "Nutanix": 8, "VMware": 7, "KVM": 6,
        "Proxmox": 6, "Hyper-V": 5,
        "Cisco": 5, "Routing": 4, "Switching": 4,
        "RAID": 4, "NFS": 4,
        "Zabbix": 4, "Nagios": 4,
        "Docker": 3, "Kubernetes": 4,
    },

    "Soporte Técnico": {
        "Active Directory": 6, "Windows Server": 6,
        "Linux": 4, "DNS": 4, "DHCP": 4,
        "Firewall": 4, "VPN": 4,
        "Backup": 4, "PowerShell": 4,
    },

    "Data Science": {
        "Machine Learning": 7, "Deep Learning": 7,
        "TensorFlow": 6, "PyTorch": 6,
        "scikit-learn": 6, "XGBoost": 5, "LightGBM": 5,
        "NLP": 6, "BERT": 6, "Computer Vision": 6,
        "Pandas": 4, "NumPy": 4, "Jupyter": 3,
        "Apache Spark": 5, "Hadoop": 5,
        "dbt": 4, "Apache Airflow": 4,
        "ETL": 3, "Data Warehouse": 4,
        "R": 5,
    },

    "QA": {
        "Selenium": 7, "Cypress": 7, "Playwright": 7,
        "Appium": 7, "PyTest": 5, "JUnit": 5,
        "Cucumber": 5, "JMeter": 5,
        "Testing": 4, "Postman": 3,
    },

    "Seguridad": {
        "OSCP": 9, "CEH": 8, "Security+": 7,
        "Ethical Hacking": 9, "Pentesting": 9,
        "Red Team": 8, "Blue Team": 7,
        "SIEM": 7, "SOC": 7,
        "OWASP": 6, "Zero Trust": 6,
        "Cybersecurity": 5, "Vulnerability Assessment": 6,
        "NGFW": 5, "NAC": 5,
        "Malware Analysis": 7, "IDS/IPS": 4,
    },

    "Diseño": {
        "Figma": 7, "Sketch": 6, "Adobe XD": 6,
        "Photoshop": 5, "Illustrator": 5,
        "Design System": 6, "UX Research": 6,
        "Wireframes": 5, "Prototyping": 5,
        "Motion Design": 5,
    },

    "Fullstack": {
        "React": 3, "Next.js": 4, "Vue.js": 3,
        "Node.js": 3, "Django": 3, "Rails": 3,
        "PostgreSQL": 2, "MongoDB": 2,
        "Docker": 2, "AWS": 2,
    },
}


# =========================================================
# HYBRID PROFILE BONUSES
# These stacks are strong signals for specific combos.
# Applied AFTER individual scoring.
# =========================================================

HYBRID_BONUSES: List[Tuple[List[str], str, float, str]] = [
    # (required_skills,  primary_area,  bonus,  label)

    # Backend + DevOps
    (["Docker", "Node.js"],          "DevOps",   2.0, "Backend+DevOps"),
    (["Docker", "Python"],           "DevOps",   2.0, "Backend+DevOps"),
    (["Kubernetes", "Docker"],       "DevOps",   3.0, "Backend+DevOps"),

    # Networking + Linux
    (["CCNA", "Linux"],              "Networking", 4.0, "Networking+Linux"),
    (["Cisco", "Routing", "Linux"],  "Networking", 4.0, "Networking+Linux"),
    (["Mikrotik", "Linux"],          "Networking", 3.0, "Networking+Linux"),

    # Networking + SysAdmin
    (["CCNA", "Windows Server"],     "SysAdmin",  2.0, "Networking+SysAdmin"),
    (["Routing", "Active Directory"],"SysAdmin",  2.0, "Networking+SysAdmin"),

    # SysAdmin + Cloud
    (["VMware", "AWS"],              "Cloud Computing", 3.0, "SysAdmin+Cloud"),
    (["VMware", "Azure"],            "Cloud Computing", 3.0, "SysAdmin+Cloud"),
    (["Ansible", "Terraform"],       "DevOps",    3.0, "SysAdmin+DevOps"),

    # Fullstack
    (["React", "Node.js", "PostgreSQL"], "Fullstack", 4.0, "Fullstack"),
    (["Vue.js", "Django"],           "Fullstack", 3.0, "Fullstack"),
    (["React", "Django"],            "Fullstack", 3.0, "Fullstack"),
    (["Next.js", "Node.js"],         "Fullstack", 3.0, "Fullstack"),

    # Frontend + UX
    (["Figma", "React"],             "Diseño",    2.0, "Frontend+UX"),
    (["Figma", "UX Research"],       "Diseño",    4.0, "Frontend+UX"),

    # Security + Networking
    (["Palo Alto", "Firewall"],      "Seguridad", 3.0, "Security+Net"),
    (["OWASP", "Pentesting"],        "Seguridad", 3.0, "Security"),
    (["SIEM", "SOC"],                "Seguridad", 4.0, "Security+SOC"),

    # Data + Backend
    (["Machine Learning", "Python"], "Data Science", 3.0, "DS+Backend"),
    (["Apache Spark", "Python"],     "Data Science", 3.0, "DS+Backend"),
]


# =========================================================
# SENIORITY KEYWORDS
# =========================================================

SENIORITY_KEYWORDS = {
    "Senior": [
        "senior", "sr.", "arquitecto", "architect",
        "tech lead", "technical lead", "lider tecnico",
        "principal engineer", "staff engineer",
        "head of engineering", "jefe de desarrollo",
        "director of engineering",
        "liderazgo", "mentoring", "mentored", "mentoreo",
        "lideré", "liderando", "dirigí", "gestioné",
        "managed team", "team of", "equipo de",
        "10 years", "9 years", "8 years",
        "10 años", "9 años", "8 años",
    ],
    "Mid": [
        "mid-level", "mid level", "ssr.", "semi senior",
        "semisenior", "semi-senior",
        "intermediate", "experienced",
        "4 years", "5 years", "6 years", "7 years",
        "4 años", "5 años", "6 años", "7 años",
        "3 años", "3 years",
    ],
    "Junior": [
        "junior", "jr.", "trainee", "intern",
        "pasante", "practicante",
        "recien graduado", "recién graduado",
        "egresado", "estudiante", "student",
        "primer empleo", "first job",
        "aprendiendo", "learning",
        "0 years", "1 year", "2 years",
        "0 años", "1 año", "2 años",
    ],
}

LEADERSHIP_KEYWORDS = [
    "tech lead", "technical lead", "lider", "líder",
    "arquitecto", "architect", "jefe", "head",
    "director", "managed", "gestioné", "dirigí",
    "lideré", "mentored", "mentoring", "mentoreo",
    "principal", "staff engineer",
]


# =========================================================
# EXPERIENCE PATTERNS
# =========================================================

EXPERIENCE_PATTERNS = [
    r"(\d+)\+?\s*(?:years?|años?|año)\s+(?:of\s+)?(?:experience|experiencia)",
    r"(?:experience|experiencia)\s+(?:of\s+)?(\d+)\+?\s*(?:years?|años?|año)",
    r"(\d+)\+?\s*(?:years?|años?|año)",
    r"mas\s+de\s+(\d+)\s*(?:years?|años?)",
    r"over\s+(\d+)\s*(?:years?|años?)",
    r"more\s+than\s+(\d+)\s*(?:years?|años?)",
]


# =========================================================
# REGEX SKILL MATCHING
# =========================================================

def _word_boundary_match(text: str, alias: str) -> bool:
    """
    Match alias with strict word boundaries.
    Handles special chars in aliases like node.js, c++, c#, ci/cd.
    """
    escaped = re.escape(alias)
    # For aliases ending in special chars (c++, c#), use \b only at start
    if re.search(r"[+#]$", alias):
        pattern = rf"(?<![a-z0-9]){escaped}(?![a-z0-9])"
    else:
        pattern = rf"(?<![a-z0-9\-]){escaped}(?![a-z0-9\-])"
    return bool(re.search(pattern, text))


def extract_skills(text: str) -> List[str]:
    """
    Extract canonical skills from CV text.
    Uses strict word-boundary matching + context gates for ambiguous tokens.
    """
    norm = normalize(text)
    found: List[str] = []

    # Main alias matching
    for canonical, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            alias_norm = normalize(alias)
            if _word_boundary_match(norm, alias_norm):
                found.append(canonical)
                break

    # Context-gated skills (Go, C++, C#, R, SQL)
    for canonical, pattern in CONTEXT_SKILLS:
        if canonical not in found:
            if re.search(pattern, norm):
                found.append(canonical)

    return sorted(set(found))


# =========================================================
# SKILLS BY CATEGORY
# =========================================================

def extract_skills_by_category(skills: List[str]) -> Dict[str, List[dict]]:
    """
    Retorna skills agrupados por categoría con identidad única por categoría.
    Cada skill incluye ID único categoría::skill para que el mismo skill
    en categorías diferentes sea independiente (ej: Linux/DevOps vs Linux/Networking).
    """
    result: Dict[str, List[dict]] = {}
    for category, cat_skills in CATEGORY_SKILLS.items():
        matched = []
        for s in skills:
            if s in cat_skills:
                matched.append({
                    "id": f"{category}::{s}",
                    "name": s,
                    "category": category,
                })
        if matched:
            result[category] = matched
    return result


# =========================================================
# EXPERIENCE EXTRACTION
# =========================================================

def extract_experience_years(text: str) -> int:
    norm = normalize(text)
    years_found = []
    for pattern in EXPERIENCE_PATTERNS:
        for match in re.finditer(pattern, norm):
            try:
                y = int(match.group(1))
                if 0 <= y <= 40:
                    years_found.append(y)
            except (IndexError, ValueError):
                pass
    return max(years_found) if years_found else 0


# =========================================================
# STUDENT / TRAINEE DETECTION
# =========================================================

_STUDENT_PATTERNS = re.compile(
    r"\b(?:student|estudiante|universidad|university|college|"
    r"semester|semestre|currently studying|actualmente cursando|"
    r"proyecto final|final project|tesis|egresado|egresada|"
    r"recien graduado|reci.n graduado|practicante|pasante|"
    r"trainee|intern\b|internship|primer empleo|first job)\b",
    re.IGNORECASE,
)

def detect_student_profile(text: str) -> bool:
    return bool(_STUDENT_PATTERNS.search(normalize(text)))


# =========================================================
# LEADERSHIP DETECTION
# =========================================================

_LEADERSHIP_PATTERN = re.compile(
    r"\b(?:tech lead|technical lead|l[ií]der|arquitecto|architect|"
    r"jefe|head of|director|managed|gestion[eé]|dirig[ií]|"
    r"lider[eé]|mentor(?:ed|ing|eo)?|principal engineer|staff engineer)\b",
    re.IGNORECASE,
)

def detect_leadership(text: str) -> bool:
    return bool(_LEADERSHIP_PATTERN.search(normalize(text)))


# =========================================================
# AREA SCORING ENGINE
# =========================================================

def calculate_area_scores(
    skills: List[str],
    text: str,
) -> Dict[str, float]:
    """
    Returns a dict of area → weighted score.
    Combines:
      1. Skill weights per area
      2. Keyword bonus rules
      3. Hybrid profile bonuses
    """
    scores: Dict[str, float] = defaultdict(float)
    norm = normalize(text)

    # ── 1. Skill weights ──────────────────────────────────
    for area, weights in AREA_WEIGHTS.items():
        for skill in skills:
            if skill in weights:
                scores[area] += weights[skill]

    # ── 2. Hard rule bonuses (high-signal combos) ─────────
    # Networking certification bonus
    if "ccna" in norm or "CCNA" in skills:
        scores["Networking"] += 10
    if "ccnp" in norm or "CCNP" in skills:
        scores["Networking"] += 14
    if "ccie" in norm or "CCIE" in skills:
        scores["Networking"] += 18

    # Cisco + routing/switching → Networking
    if "cisco" in norm and ("routing" in norm or "switching" in norm):
        scores["Networking"] += 6

    # Mikrotik → Networking
    if "mikrotik" in norm:
        scores["Networking"] += 6
        scores["SysAdmin"] += 2

    # SD-WAN / BGP / MPLS → strong Networking
    for kw in ["sd-wan", "sdwan", "bgp", "mpls", "ospf", "eigrp"]:
        if kw in norm:
            scores["Networking"] += 5

    # OSCP / CEH → Seguridad
    if "oscp" in norm or "ceh" in norm:
        scores["Seguridad"] += 10

    # Cloud certs
    for cloud_kw in ["aws certified", "gcp certified", "azure certified",
                     "cloud architect", "cloud engineer", "solutions architect"]:
        if cloud_kw in norm:
            scores["Cloud Computing"] += 8

    # SysAdmin signals
    for kw in ["vmware", "vsphere", "vcenter", "nutanix", "proxmox"]:
        if kw in norm:
            scores["SysAdmin"] += 6
            scores["Infraestructura"] += 4

    if "active directory" in norm:
        scores["SysAdmin"] += 8

    # Soporte Técnico signals
    for kw in ["soporte", "helpdesk", "help desk", "mesa de ayuda",
               "nivel 1", "nivel 2", "nivel 3",
               "nivel1", "nivel2", "nivel3",
               "tier 1", "tier 2", "tier 3",
               "escalacion", "escalation", "troubleshooting"]:
        if kw in norm:
            scores["Soporte Técnico"] += 4

    # DevOps / infra
    if "kubernetes" in norm or "k8s" in norm:
        scores["DevOps"] += 5
    if "terraform" in norm:
        scores["DevOps"] += 5
        scores["Cloud Computing"] += 3
    if "docker" in norm and ("linux" in norm or "bash" in norm):
        scores["DevOps"] += 4

    # Backend combos
    if ("nodejs" in norm or "node.js" in norm) and "express" in norm:
        scores["Backend"] += 5
    if "spring boot" in norm:
        scores["Backend"] += 5
    if "django" in norm or "fastapi" in norm or "flask" in norm:
        scores["Backend"] += 4

    # Frontend combos
    if ("react" in norm or "vue" in norm) and ("html" in norm or "css" in norm):
        scores["Frontend"] += 3
    if "next.js" in norm or "nextjs" in norm:
        scores["Frontend"] += 4

    # Data Science
    if "machine learning" in norm or "aprendizaje automatico" in norm:
        scores["Data Science"] += 7
    if "scikit-learn" in norm or "sklearn" in norm:
        scores["Data Science"] += 6

    # ── 3. Hybrid bonuses ─────────────────────────────────
    skill_set = set(skills)
    for required, area, bonus, _ in HYBRID_BONUSES:
        if all(r in skill_set for r in required):
            scores[area] += bonus

    return dict(scores)


# =========================================================
# SENIORITY HEURISTICS
# =========================================================

def _heuristic_seniority(
    text: str,
    experience_years: int,
) -> Optional[str]:
    """
    Returns seniority label based on experience + keywords.
    Returns None if undecided (defer to ML).
    """
    norm = normalize(text)

    # Hard rules on years
    if experience_years >= 7:
        return "Senior"
    if 3 <= experience_years <= 6:
        return "Mid"
    if 0 <= experience_years <= 2 and experience_years > 0:
        return "Junior"

    # Keyword signals (ordered: Senior > Mid > Junior)
    for kw in SENIORITY_KEYWORDS["Senior"]:
        if kw in norm:
            return "Senior"

    for kw in SENIORITY_KEYWORDS["Mid"]:
        if kw in norm:
            return "Mid"

    for kw in SENIORITY_KEYWORDS["Junior"]:
        if kw in norm:
            return "Junior"

    return None  # undecided → use ML


def _seniority_from_leadership(text: str, current: str) -> str:
    """Promote to Senior if strong leadership signals present."""
    if detect_leadership(text):
        return "Senior"
    return current


# =========================================================
# CONFIDENCE SCORE
# =========================================================

def _compute_confidence(
    area_scores: Dict[str, float],
    ml_proba: Optional[np.ndarray],
    ml_classes: Optional[List[str]],
    main_area: str,
    skills_count: int,
) -> float:
    """
    Hybrid confidence from:
    - Heuristic score dominance
    - ML probability for the chosen area
    - Number of skills detected
    """
    if not area_scores:
        if ml_proba is not None and ml_classes is not None and main_area in ml_classes:
            idx = list(ml_classes).index(main_area)
            return round(float(ml_proba[idx]), 3)
        return 0.40

    total = sum(area_scores.values())
    max_score = area_scores.get(main_area, 0)

    heuristic_conf = min(max_score / total, 0.98) if total > 0 else 0.40

    # Blend with ML prob if available
    if ml_proba is not None and ml_classes is not None and main_area in list(ml_classes):
        idx = list(ml_classes).index(main_area)
        ml_conf = float(ml_proba[idx])
        confidence = 0.6 * heuristic_conf + 0.4 * ml_conf
    else:
        confidence = heuristic_conf

    # Slight boost for many skills detected (more evidence)
    if skills_count >= 8:
        confidence = min(confidence + 0.04, 0.99)
    elif skills_count >= 5:
        confidence = min(confidence + 0.02, 0.99)

    return round(confidence, 3)


# =========================================================
# MAIN PREDICT FUNCTION
# =========================================================

def predict_candidate(text: str) -> dict:
    
    """
    Full hybrid CV parsing.

    Returns:
        {
          "main_area":         str,
          "secondary_areas":   [{"area": str, "score": float}],
          "ml_area":           str,
          "seniority":         str,
          "experience_years":  int,
          "skills":            [str],
          "skills_by_category": {str: [str]},
          "confidence":        float,
          "area_scores":       {str: float},
          "student_profile":   bool,
          "leadership":        bool,
          "hybrid_profiles":   [str],
        }
    """
    if _area_model is None or _seniority_model is None:
        raise RuntimeError("Models not loaded. Call load_models() first.")

    norm = normalize(text)

    if not norm.strip():
        raise ValueError("Texto vacío")

    # ── ML predictions ─────────────────────────────────────
    ml_area = _area_model.predict([norm])[0]
    ml_sen  = _seniority_model.predict([norm])[0]

    # ML probabilities (available because we used CalibratedClassifierCV)
    ml_proba: Optional[np.ndarray] = None
    ml_classes: Optional[List[str]] = None
    try:
        ml_proba   = _area_model.predict_proba([norm])[0]
        ml_classes = list(_area_model.classes_)
    except Exception:
        pass

    # ── Skills ─────────────────────────────────────────────
    skills = extract_skills(text)
    skills_by_cat = extract_skills_by_category(skills)

    # ── Experience ─────────────────────────────────────────
    experience_years = extract_experience_years(text)

    # ── Area scoring ───────────────────────────────────────
    area_scores = calculate_area_scores(skills, text)

    # Blend ML area probability into scores for softer override
    if ml_proba is not None and ml_classes is not None:
        ml_max_idx   = int(np.argmax(ml_proba))
        ml_top_area  = ml_classes[ml_max_idx]
        ml_top_prob  = float(ml_proba[ml_max_idx])
        # Add ML signal as a fractional bonus proportional to confidence
        ml_bonus = ml_top_prob * 12  # scale factor
        area_scores[ml_top_area] = area_scores.get(ml_top_area, 0) + ml_bonus

    # ── Determine main area ────────────────────────────────
    if area_scores:
        main_area = max(area_scores, key=area_scores.get)
    else:
        main_area = ml_area

    # ── Secondary areas ────────────────────────────────────
    secondary_areas = sorted(
        [
            {"area": area, "score": float(round(score, 2))}
            for area, score in area_scores.items()
            if area != main_area and score > 0
        ],
        key=lambda x: x["score"],
        reverse=True,
    )[:4]  # top 4 secondary

    # ── Seniority ──────────────────────────────────────────
    heuristic_sen = _heuristic_seniority(text, experience_years)
    seniority = heuristic_sen if heuristic_sen else ml_sen

    # Student override (always Junior)
    if detect_student_profile(text):
        seniority = "Junior"

    # Leadership promotion (→ Senior)
    if detect_leadership(text) and seniority != "Senior":
        seniority = "Senior"

    # ── Hybrid profiles ────────────────────────────────────
    skill_set = set(skills)
    hybrid_profiles: List[str] = []
    seen_labels: set = set()
    for required, _, _, label in HYBRID_BONUSES:
        if all(r in skill_set for r in required) and label not in seen_labels:
            hybrid_profiles.append(label)
            seen_labels.add(label)

    # ── Confidence ─────────────────────────────────────────
    confidence = _compute_confidence(
        area_scores, ml_proba, ml_classes, main_area, len(skills)
    )

    return {
        "main_area":          main_area,
        "secondary_areas":    secondary_areas,
        "ml_area":            ml_area,
        "seniority":          seniority,
        "experience_years":   experience_years,
        "skills":             skills,
        "skills_by_category": skills_by_cat,
        "primary_skills_by_category": _primary_skills_by_category(skills, main_area, area_scores),
        "confidence": float(confidence),
        "area_scores":        {k: float(round(v, 2)) for k, v in sorted(
                                   area_scores.items(), key=lambda x: x[1], reverse=True
                               )},
        "student_profile":    detect_student_profile(text),
        "leadership":         detect_leadership(text),
        "hybrid_profiles":    hybrid_profiles,
    }


# =========================================================
# CLI / DEMO  — python predict.py
# =========================================================

if __name__ == "__main__":
    import json

    load_models()

    TEST_CVS = [
        {
            "label": "Backend Junior",
            "text": """
                Estudiante de Ingeniería en Sistemas. Proyectos con Node.js,
                Express y PostgreSQL. Autenticación JWT. APIs REST. Git, Docker básico.
            """,
        },
        {
            "label": "Backend Senior",
            "text": """
                Senior backend engineer. 9 years designing distributed systems.
                Java Spring Boot, Apache Kafka, PostgreSQL, Kubernetes.
                Led team of 7 engineers, mentored 3 juniors.
                Microservices architecture, event-driven design.
            """,
        },
        {
            "label": "Networking Mid",
            "text": """
                Técnico de redes CCNA. 4 años administrando infraestructura
                Cisco y Mikrotik. Diseño de VLANs, routing OSPF y BGP,
                troubleshooting de conectividad. TCP/IP, DNS, DHCP.
            """,
        },
        {
            "label": "DevOps Senior",
            "text": """
                Senior DevOps engineer. Kubernetes, Terraform, ArgoCD, GitOps.
                AWS, GCP. CI/CD with GitHub Actions and Jenkins.
                Docker, Helm, Prometheus, Grafana. Linux. Led infra team of 6.
            """,
        },
        {
            "label": "Frontend Mid",
            "text": """
                Frontend developer 4 years. React, TypeScript, Next.js, TailwindCSS.
                Redux, Vite, SASS. REST API integrations. Performance optimization.
            """,
        },
        {
            "label": "SysAdmin Mid",
            "text": """
                Administrador de sistemas Linux y Windows Server. 5 años.
                VMware vSphere, Ansible, Zabbix, Active Directory, Group Policy.
                Backup, iptables, Nginx, SSH. Bash scripting.
            """,
        },
        {
            "label": "Data Scientist Mid",
            "text": """
                Data scientist. Python, scikit-learn, XGBoost, pandas, NumPy.
                Machine learning models for churn prediction and NLP.
                Jupyter, Matplotlib, Seaborn. SQL, PostgreSQL.
            """,
        },
        {
            "label": "Security Senior",
            "text": """
                Penetration tester senior. OSCP, CEH. Red team operations,
                custom exploit development, social engineering, phishing simulations.
                SIEM, SOC analysis, vulnerability assessment. OWASP, Zero Trust.
            """,
        },
        {
            "label": "Fullstack Mid",
            "text": """
                Fullstack developer. React, TypeScript, Node.js, PostgreSQL.
                Docker, AWS, GitHub Actions. REST API design, JWT auth.
                4 years building SaaS products.
            """,
        },
        {
            "label": "Networking+Linux Hybrid",
            "text": """
                Técnico redes y sistemas. CCNA. Linux Ubuntu, Bash scripting,
                SSH. Cisco routers, Mikrotik, VLANs, routing.
                Soporte técnico nivel 2. 3 años de experiencia.
            """,
        },
    ]

    print("\n" + "=" * 65)
    print("  ADVANCED CV PARSER — DEMO")
    print("=" * 65)

    for cv in TEST_CVS:
        result = predict_candidate(cv["text"])
        print(f"\n[{cv['label']}]")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print("-" * 65)

def _primary_skills_by_category(skills: list, main_area: str, area_scores: dict) -> dict:
    """
    Asigna cada skill a UNA sola categoría:
    1. Si está en CATEGORY_SKILLS, usa la categoría más relevante según el perfil
    2. Si no está mapeado, queda en "Otros" para no perderlo
    """
    result: dict = {}
    
    sorted_categories = sorted(
        area_scores.keys(),
        key=lambda c: area_scores.get(c, 0),
        reverse=True
    )
    if main_area in sorted_categories:
        sorted_categories.remove(main_area)
        sorted_categories.insert(0, main_area)

    assigned = set()
    
    for category in sorted_categories:
        cat_skills = CATEGORY_SKILLS.get(category, [])
        for skill in skills:
            if skill in cat_skills and skill not in assigned:
                result.setdefault(category, []).append(skill)
                assigned.add(skill)
    
    unmapped = [s for s in skills if s not in assigned]
    if unmapped:
        result['Otros'] = sorted(unmapped)
    
    return result