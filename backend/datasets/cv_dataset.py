import pandas as pd
import os

data = [


    {
        "text": "Estudiante de Ingeniería en Sistemas con proyectos backend desarrollados en Node.js y Express. Experiencia básica con APIs REST y bases de datos PostgreSQL.",
        "area": "Backend", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Junior backend developer learning Node.js, Express and MongoDB. Built small REST APIs for academic projects.",
        "area": "Backend", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Recién graduado de Informática. Proyectos universitarios con Python, Flask y SQLite. Ganas de aprender y crecer en backend.",
        "area": "Backend", "seniority": "Junior", "experience_years": 0
    },
    {
        "text": "Trainee backend con conocimientos en Java, Spring Boot básico y MySQL. Trabajo en equipo, metodologías ágiles.",
        "area": "Backend", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Computer science student with projects in Python, Django and PostgreSQL. Experience with JWT authentication and REST API design.",
        "area": "Backend", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Egresado de Sistemas. Desarrollo de una API REST con Node.js y Express para gestión de usuarios. Base de datos MySQL.",
        "area": "Backend", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Pasante en empresa de software. Tareas de mantenimiento backend en PHP Laravel. Consultas SQL, migraciones y debugging.",
        "area": "Backend", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Junior Python developer with experience in FastAPI and SQLAlchemy. Built REST endpoints for a small e-commerce project.",
        "area": "Backend", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Desarrollador junior Node.js. Integración de APIs externas, manejo de autenticación JWT, despliegue básico en Linux.",
        "area": "Backend", "seniority": "Junior", "experience_years": 2
    },
    {
        "text": "Backend trainee working with Ruby on Rails. Created CRUD endpoints, wrote unit tests and managed PostgreSQL migrations.",
        "area": "Backend", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Estudiante avanzado de TI con proyecto final en Django REST Framework. Autenticación con JWT, documentación con Swagger.",
        "area": "Backend", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Primer empleo en startup. Mantenimiento de microservicio en Node.js, resolución de bugs, revisión de PRs, integración con Redis.",
        "area": "Backend", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Junior backend engineer. Experience with Express.js, REST APIs, Postgres, Git. Eager to grow in scalable systems architecture.",
        "area": "Backend", "seniority": "Junior", "experience_years": 2
    },
    {
        "text": "Practicante en empresa de desarrollo web. Trabajo con PHP, Laravel y MySQL. Integración con APIs de pagos.",
        "area": "Backend", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Self-taught backend developer. Created REST APIs using Node.js and MongoDB. Deployed on Linux VPS with Nginx.",
        "area": "Backend", "seniority": "Junior", "experience_years": 1
    },


    {
        "text": "Backend developer with 4 years of experience building REST APIs using Node.js, Express and PostgreSQL. Worked with JWT and OAuth authentication systems.",
        "area": "Backend", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Desarrollador backend con experiencia en Python, FastAPI y PostgreSQL. Diseño de microservicios, integración con Redis y despliegue con Docker.",
        "area": "Backend", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "PHP Laravel developer with 3 years building web applications. REST APIs, MySQL, Redis caching, and unit testing with PHPUnit.",
        "area": "Backend", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": "Backend engineer using Java Spring Boot. Desarrollé servicios REST, integraciones con Kafka y despliegue en contenedores Docker.",
        "area": "Backend", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Node.js backend developer. 4 years building scalable APIs, working with MongoDB, Redis and AWS Lambda serverless functions.",
        "area": "Backend", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Desarrollador Python mid-level. Trabajo con Django REST Framework, Celery para tareas asíncronas y PostgreSQL. Experiencia en startups.",
        "area": "Backend", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Backend developer. 3 years with Go (Golang), building high-performance REST services. PostgreSQL, Docker, GitHub Actions CI/CD.",
        "area": "Backend", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": "Ingeniero backend con foco en APIs REST usando Node.js y Express. Trabajo con bases de datos relacionales y no relacionales, autenticación OAuth2.",
        "area": "Backend", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "Mid backend engineer. Spring Boot microservices, Kafka messaging, Docker, PostgreSQL. Agile teams, code reviews, CI/CD pipelines.",
        "area": "Backend", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Python backend developer with Django and FastAPI. Built payment integration APIs, async task queues with Celery, monitoring with Datadog.",
        "area": "Backend", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "Desarrollador backend Node.js. Diseño e implementación de APIs RESTful, integración con sistemas de pagos, optimización de queries PostgreSQL.",
        "area": "Backend", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Ruby on Rails developer. 4 years building SaaS backends. PostgreSQL, Redis, Sidekiq, API design, testing with RSpec.",
        "area": "Backend", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Desarrollador mid-level PHP. Laravel, MySQL, Redis, APIs REST. Trabaje en proyectos de e-commerce con altas cargas de usuarios.",
        "area": "Backend", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "Backend engineer focused on Node.js and TypeScript. 3 years building modular REST APIs, integrating third-party services and writing integration tests.",
        "area": "Backend", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": "Desarrollador Java backend con 5 años de experiencia. Spring Boot, microservicios, Oracle DB, Apache Kafka, Docker Compose.",
        "area": "Backend", "seniority": "Mid", "experience_years": 5
    },


    {
        "text": "Senior backend engineer with 9 years of experience designing distributed systems using Java Spring Boot, Kafka, PostgreSQL and Kubernetes.",
        "area": "Backend", "seniority": "Senior", "experience_years": 9
    },
    {
        "text": "Arquitecto backend senior. Diseño de microservicios con Node.js, event-driven architecture con Kafka, liderazgo técnico de equipos de 5+ developers.",
        "area": "Backend", "seniority": "Senior", "experience_years": 10
    },
    {
        "text": "Senior Python engineer. Built and maintained high-traffic Django APIs serving 10M+ requests/day. PostgreSQL optimization, Redis, Elasticsearch.",
        "area": "Backend", "seniority": "Senior", "experience_years": 8
    },
    {
        "text": "Lead backend developer con 10 años de experiencia. Node.js, Go, PostgreSQL, Kafka. Mentor de equipos junior y mid. Arquitectura de sistemas escalables.",
        "area": "Backend", "seniority": "Senior", "experience_years": 10
    },
    {
        "text": "Senior Java architect. Designed microservices with Spring Boot, Spring Cloud, Kubernetes and AWS EKS. Team of 12 engineers.",
        "area": "Backend", "seniority": "Senior", "experience_years": 12
    },
    {
        "text": "Backend tech lead. 8 años construyendo plataformas SaaS con Node.js, Python, arquitecturas hexagonales y DDD. Liderazgo técnico y revisiones de código.",
        "area": "Backend", "seniority": "Senior", "experience_years": 8
    },
    {
        "text": "Senior backend engineer specializing in Go microservices. gRPC, Kafka, PostgreSQL, Redis. Built payment processing platform handling $1B+ monthly transactions.",
        "area": "Backend", "seniority": "Senior", "experience_years": 9
    },
    {
        "text": "Desarrollador senior backend con experiencia en Python, FastAPI y arquitectura de microservicios. Liderazgo técnico, mentoring y optimización de sistemas de alto tráfico.",
        "area": "Backend", "seniority": "Senior", "experience_years": 8
    },
    {
        "text": "Senior software engineer. 11 years with Java Spring, Hibernate, Oracle, Kafka. Enterprise-level backend systems in banking and fintech.",
        "area": "Backend", "seniority": "Senior", "experience_years": 11
    },
    {
        "text": "Senior Node.js engineer. Lideré la migración de monolito a microservicios. Docker, Kubernetes, Redis, Elasticsearch. Equipos distribuidos.",
        "area": "Backend", "seniority": "Senior", "experience_years": 8
    },


    {
        "text": "Junior frontend developer with knowledge of HTML, CSS and JavaScript. Created responsive landing pages and small React components.",
        "area": "Frontend", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Estudiante de diseño web. HTML, CSS, JavaScript básico. Creación de páginas responsivas con Bootstrap y Flexbox.",
        "area": "Frontend", "seniority": "Junior", "experience_years": 0
    },
    {
        "text": "Junior React developer. Built simple SPAs with React and Context API. Consumed REST APIs and styled with TailwindCSS.",
        "area": "Frontend", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Practicante frontend. Trabajo con HTML, CSS, JavaScript y Vue.js básico. Corrección de bugs y mejoras de UI.",
        "area": "Frontend", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Self-taught frontend developer. Built personal projects with React, styled-components and REST API consumption.",
        "area": "Frontend", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Recién egresado. Proyecto de grado con Angular y TypeScript. Conexión a APIs REST, formularios reactivos y manejo de rutas.",
        "area": "Frontend", "seniority": "Junior", "experience_years": 0
    },
    {
        "text": "Junior developer con enfoque en React y Next.js. Trabajo en proyectos freelance de landing pages y sitios estáticos.",
        "area": "Frontend", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Frontend trainee. HTML, CSS, JavaScript, React básico. Pasantía en agencia digital. Creación de componentes de UI.",
        "area": "Frontend", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Junior frontend engineer. React, TypeScript, TailwindCSS. Integrated REST APIs, handled form validations, deployed on Vercel.",
        "area": "Frontend", "seniority": "Junior", "experience_years": 2
    },
    {
        "text": "Desarrollador frontend junior. Vue.js, Vuex, HTML, CSS, SASS. Trabajo en equipo con metodologías ágiles, Git y revisión de código.",
        "area": "Frontend", "seniority": "Junior", "experience_years": 1
    },


    {
        "text": "Frontend developer specialized in React, TailwindCSS and TypeScript. Built responsive interfaces connected to REST APIs.",
        "area": "Frontend", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Vue.js frontend engineer using Tailwind, Vite and TypeScript in SPA applications. 3 years of experience.",
        "area": "Frontend", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": "Desarrollador frontend mid-level. React, Redux Toolkit, TypeScript, Next.js. Optimización de performance, SEO y accesibilidad.",
        "area": "Frontend", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Angular developer with 4 years building enterprise dashboards. TypeScript, RxJS, NgRx, REST API integration.",
        "area": "Frontend", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Frontend engineer. React, Next.js, GraphQL, Styled Components. 4 years working in product teams with designers and backend engineers.",
        "area": "Frontend", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Desarrollador React con 3 años de experiencia. Redux, React Query, TailwindCSS, testing con Jest y React Testing Library.",
        "area": "Frontend", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": "Mid Vue.js developer. Vuex, Vue Router, Vite, Composition API. Built complex admin panels for SaaS platforms.",
        "area": "Frontend", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": "Frontend developer con experiencia en Angular, TypeScript y Material UI. Trabajo en proyectos enterprise con equipos ágiles.",
        "area": "Frontend", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "React and Next.js developer. 4 years building e-commerce frontends. Performance optimization, Lighthouse scores, SSR/SSG.",
        "area": "Frontend", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Desarrollador frontend mid. Vue 3, Pinia, Vite, TypeScript, TailwindCSS. Trabajo en startups y proyectos freelance de mediana complejidad.",
        "area": "Frontend", "seniority": "Mid", "experience_years": 3
    },


    {
        "text": "Senior frontend engineer with 8 years of experience. React, TypeScript, Next.js. Led frontend architecture migrations, mentored junior developers.",
        "area": "Frontend", "seniority": "Senior", "experience_years": 8
    },
    {
        "text": "Lead frontend developer. 9 años con React, Vue, Angular. Definición de arquitectura frontend, Design Systems, mentoring de equipos.",
        "area": "Frontend", "seniority": "Senior", "experience_years": 9
    },
    {
        "text": "Senior React engineer. Micro-frontends architecture, Module Federation, GraphQL, TypeScript, testing strategy. 8 years in product companies.",
        "area": "Frontend", "seniority": "Senior", "experience_years": 8
    },
    {
        "text": "Frontend tech lead. 10 años liderando equipos. Arquitectura de aplicaciones complejas en Angular. Revisión de código, mentoring senior y definición de estándares.",
        "area": "Frontend", "seniority": "Senior", "experience_years": 10
    },
    {
        "text": "Senior frontend developer specialized in performance optimization. React, Next.js, Webpack, Core Web Vitals. Reduced load times by 60%.",
        "area": "Frontend", "seniority": "Senior", "experience_years": 7
    },


    {
        "text": "Junior DevOps with Linux basics, Git, Docker and server management. Learning CI/CD pipelines and cloud fundamentals.",
        "area": "DevOps", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Estudiante de sistemas con interés en DevOps. Practicas con Docker, Bash scripting y GitHub Actions en proyectos personales.",
        "area": "DevOps", "seniority": "Junior", "experience_years": 0
    },
    {
        "text": "Junior Linux admin. Mantenimiento de servidores, scripts Bash, configuración de servicios Nginx. Aprendiendo Docker y Terraform.",
        "area": "DevOps", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "DevOps trainee. Docker, Linux, GitHub Actions basics. Assisted senior engineers with deployments and monitoring setup.",
        "area": "DevOps", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Recién egresado interesado en DevOps. Experiencia con Docker Compose, scripts Bash y administración básica de servidores Ubuntu.",
        "area": "DevOps", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Junior cloud engineer. AWS fundamentals, EC2, S3, IAM. Basic Terraform scripts, Docker containerization for dev environments.",
        "area": "DevOps", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Pasante DevOps. Automatización de deploys con GitHub Actions, administración Linux, monitoreo con Grafana y Prometheus.",
        "area": "DevOps", "seniority": "Junior", "experience_years": 1
    },


    {
        "text": "Linux administrator with experience using SSH, GitHub Actions and Docker deployments on VPS servers.",
        "area": "DevOps", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "DevOps engineer. Docker, Kubernetes, AWS, Terraform. Manage CI/CD pipelines with Jenkins and GitHub Actions. Linux administration.",
        "area": "DevOps", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "Ingeniero DevOps con 4 años de experiencia. Docker Compose, Kubernetes, Ansible, Terraform, pipelines CI/CD, monitoreo con Prometheus.",
        "area": "DevOps", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Cloud engineer. AWS (EC2, RDS, Lambda, EKS), Terraform, Docker, GitHub Actions. 4 years building cloud-native infrastructure.",
        "area": "DevOps", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "DevOps mid-level. Administración de clusters Kubernetes, Helm charts, Nginx ingress, Grafana y ELK stack para monitoreo.",
        "area": "DevOps", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": "Site Reliability Engineer. Linux, Docker, Kubernetes, Terraform, Datadog. Automated deployments and incident response.",
        "area": "DevOps", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Especialista DevOps. Pipelines con GitLab CI, despliegues Blue-Green, Docker Swarm, gestión de secretos con Vault.",
        "area": "DevOps", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "Azure DevOps engineer. Azure Pipelines, AKS, ARM Templates, Terraform, GitHub Actions. 4 years in enterprise environments.",
        "area": "DevOps", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Ingeniero de infraestructura cloud. AWS, Terraform, Ansible, Docker, Kubernetes. Automatización de aprovisionamiento y despliegue continuo.",
        "area": "DevOps", "seniority": "Mid", "experience_years": 4
    },


    {
        "text": "Senior DevOps engineer with 8 years. Docker, Kubernetes, AWS, Terraform, Jenkins, Ansible. Led infrastructure automation for teams of 50+ engineers.",
        "area": "DevOps", "seniority": "Senior", "experience_years": 8
    },
    {
        "text": "Arquitecto cloud senior. AWS, GCP, Terraform, Kubernetes, service mesh Istio. Liderazgo de migración de infraestructura on-premise a cloud.",
        "area": "DevOps", "seniority": "Senior", "experience_years": 10
    },
    {
        "text": "Senior SRE. Defined SLOs, error budgets, incident management. Kubernetes, Terraform, Prometheus, Grafana, PagerDuty. 9 years.",
        "area": "DevOps", "seniority": "Senior", "experience_years": 9
    },
    {
        "text": "Lead DevOps engineer. 10 años gestionando plataformas críticas. Multi-cloud AWS/Azure, Kubernetes, GitOps con ArgoCD, mentoring de equipos.",
        "area": "DevOps", "seniority": "Senior", "experience_years": 10
    },
    {
        "text": "Senior platform engineer. Designed internal developer platforms using Backstage, Kubernetes, Terraform Cloud. Reduced deployment times by 80%.",
        "area": "DevOps", "seniority": "Senior", "experience_years": 8
    },


    {
        "text": "CCNA student with knowledge of routing, switching, VLANs and Cisco network infrastructure. Experience configuring routers and switches.",
        "area": "Networking", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Estudiante de redes. Configuración básica de routers Cisco, switches, VLANs y protocolos TCP/IP. Cursando CCNA.",
        "area": "Networking", "seniority": "Junior", "experience_years": 0
    },
    {
        "text": "Junior network technician. Configured Cisco routers and switches. VLAN setup, DHCP configuration, basic firewall rules.",
        "area": "Networking", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Técnico de redes junior. Instalación de cableado estructurado, configuración de switches Cisco y Mikrotik, soporte LAN/WAN.",
        "area": "Networking", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Egresado de telecomunicaciones. Configuración de routers Mikrotik, administración DNS/DHCP, soporte de conectividad para empresa local.",
        "area": "Networking", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Entry-level network engineer. CCNA coursework completed. Hands-on lab experience with Cisco IOS, routing protocols OSPF, RIP.",
        "area": "Networking", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Soporte técnico en empresa ISP. Configuración de routers domésticos, diagnóstico de conectividad, ticketing, soporte telefónico.",
        "area": "Networking", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Junior network support. Troubleshooting LAN issues, VLAN configuration on Cisco Catalyst switches, cable patching.",
        "area": "Networking", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Técnico junior redes. Mantenimiento de cableado estructurado, configuración de APs WiFi, administración de switches managed.",
        "area": "Networking", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Estudiante CCNA. Simulaciones en Packet Tracer, configuración de OSPF, VLANs, STP, SSH en equipos Cisco.",
        "area": "Networking", "seniority": "Junior", "experience_years": 0
    },


    {
        "text": "Network administrator managing DNS, DHCP, firewalls and Mikrotik infrastructure. 5 years of experience.",
        "area": "Networking", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "Administrador de redes Cisco. Configuración de routers, switches, VLANs, OSPF, BGP. Gestión de infraestructura de red empresarial.",
        "area": "Networking", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "Network engineer with 4 years. Cisco routing and switching, firewall management (Fortinet, pfSense), VPN setup, network monitoring.",
        "area": "Networking", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Ingeniero de redes. Administración Cisco, Mikrotik, VLANs, QoS, BGP. Gestión de ISP regional con más de 1000 clientes.",
        "area": "Networking", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "Network administrator. DNS, DHCP, VPN, firewall (pfSense, Cisco ASA). Managed campus network with 500+ endpoints.",
        "area": "Networking", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Especialista en infraestructura de red. Cisco IOS, OSPF, BGP, Mikrotik RouterOS. Diseño y mantenimiento de topologías LAN/WAN.",
        "area": "Networking", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "Wireless network engineer. 4 years deploying Ubiquiti and Cisco Meraki networks. Hotspot management, RADIUS, captive portals.",
        "area": "Networking", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Administrador Mikrotik. CHR, RouterOS, BGP, OSPF, MPLS, gestión de ancho de banda, queues, firewall. ISP.",
        "area": "Networking", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Network operations center engineer. Monitoring with Zabbix, SNMP, troubleshooting BGP routing issues, incident management.",
        "area": "Networking", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Ingeniero de redes corporativas. Cisco Catalyst, Meraki, Fortinet. Segmentación VLAN, ACLs, políticas QoS y VPN IPSec.",
        "area": "Networking", "seniority": "Mid", "experience_years": 5
    },


    {
        "text": "Senior network engineer with enterprise networking experience. Cisco routing, switching, BGP, MPLS, firewall policy design.",
        "area": "Networking", "seniority": "Senior", "experience_years": 8
    },
    {
        "text": "Arquitecto de red senior. Diseño de topologías WAN/LAN para empresa multinacional. Cisco, Juniper, BGP, MPLS, SD-WAN.",
        "area": "Networking", "seniority": "Senior", "experience_years": 10
    },
    {
        "text": "Senior network architect. BGP, MPLS, OSPF, SD-WAN, Fortinet security policies. Led network redesign for 3000+ user campus.",
        "area": "Networking", "seniority": "Senior", "experience_years": 12
    },
    {
        "text": "Lead network engineer. 10 años diseñando y administrando redes complejas. Cisco, Juniper, Aruba. Mentoring de técnicos junior.",
        "area": "Networking", "seniority": "Senior", "experience_years": 10
    },
    {
        "text": "Senior NOC engineer. Monitored and managed backbone network. BGP peering, DDoS mitigation, 99.99% uptime SLA.",
        "area": "Networking", "seniority": "Senior", "experience_years": 9
    },


    {
        "text": "Junior data analyst using Python, Jupyter notebooks and SQL queries. Learning pandas, numpy and matplotlib.",
        "area": "Data Science", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Estudiante de ciencias de datos. Python, pandas, scikit-learn. Proyectos de análisis exploratorio y visualización de datos.",
        "area": "Data Science", "seniority": "Junior", "experience_years": 0
    },
    {
        "text": "Junior data scientist. Built regression and classification models with scikit-learn. Worked with CSV datasets and SQL databases.",
        "area": "Data Science", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Trainee en análisis de datos. Excel avanzado, SQL, Python básico. Dashboards en Power BI para reportes de ventas.",
        "area": "Data Science", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Recién egresado de estadística. Modelos predictivos con R y Python. Regresión lineal, árboles de decisión, validación cruzada.",
        "area": "Data Science", "seniority": "Junior", "experience_years": 0
    },
    {
        "text": "Junior ML engineer. Built sentiment analysis pipeline using NLP, TF-IDF and Naive Bayes classifier. Python, scikit-learn.",
        "area": "Data Science", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Pasante de análisis de datos. SQL, pandas, matplotlib, seaborn. Limpieza y análisis de datasets para equipo de marketing.",
        "area": "Data Science", "seniority": "Junior", "experience_years": 1
    },


    {
        "text": "Machine learning engineer using scikit-learn, pandas and NumPy for predictive analytics systems.",
        "area": "Data Science", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Data scientist con 4 años. Python, pandas, scikit-learn, XGBoost. Modelos de churn prediction, segmentación de clientes.",
        "area": "Data Science", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "ML engineer. TensorFlow, Keras, scikit-learn. Built image classification models for manufacturing defect detection.",
        "area": "Data Science", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Científico de datos mid-level. Series temporales con Prophet y ARIMA. Análisis de datos financieros, visualizaciones con Plotly.",
        "area": "Data Science", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "NLP engineer. 4 years building text classification, NER and summarization systems. spaCy, transformers (BERT), TF-IDF.",
        "area": "Data Science", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Data engineer with Python, Spark, Airflow, PostgreSQL. Building ETL pipelines and data lakes for analytics teams.",
        "area": "Data Science", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Analista de datos mid. SQL avanzado, Python, pandas, Power BI, Tableau. Reporting automatizado para dirección comercial.",
        "area": "Data Science", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": "Computer vision engineer. PyTorch, OpenCV, YOLO. Built object detection models for retail analytics applications.",
        "area": "Data Science", "seniority": "Mid", "experience_years": 4
    },


    {
        "text": "Deep learning researcher using PyTorch, TensorFlow and computer vision techniques. 8 years of experience.",
        "area": "Data Science", "seniority": "Senior", "experience_years": 8
    },
    {
        "text": "Senior ML engineer. Led development of recommendation systems serving 5M+ users. Spark, TensorFlow, MLflow, Kubeflow.",
        "area": "Data Science", "seniority": "Senior", "experience_years": 8
    },
    {
        "text": "Principal data scientist. 10 años. NLP, LLM fine-tuning, RAG architectures. Liderazgo técnico de equipos de ciencia de datos.",
        "area": "Data Science", "seniority": "Senior", "experience_years": 10
    },
    {
        "text": "Senior data engineer. Designed petabyte-scale data platforms using Spark, Kafka, Airflow, Databricks, Delta Lake.",
        "area": "Data Science", "seniority": "Senior", "experience_years": 9
    },
    {
        "text": "Lead data scientist. Modelos de fraud detection en tiempo real. Feature engineering avanzado, XGBoost, LightGBM, MLflow.",
        "area": "Data Science", "seniority": "Senior", "experience_years": 8
    },


    {
        "text": "Junior QA analyst performing manual testing, bug reporting and API testing with Postman.",
        "area": "QA", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Tester junior. Pruebas funcionales manuales, redacción de casos de prueba, seguimiento de defectos con Jira.",
        "area": "QA", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "QA trainee. Manual testing of web applications, API testing with Postman, test case documentation.",
        "area": "QA", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Recién egresado interesado en QA. Testing manual, básico de Selenium, documentación de bugs, métricas de calidad.",
        "area": "QA", "seniority": "Junior", "experience_years": 0
    },
    {
        "text": "Junior QA engineer. Basic Cypress E2E tests, manual regression testing, test plan writing. Worked in Scrum teams.",
        "area": "QA", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Analista QA junior. Pruebas de regresión, smoke testing, integración continua básica, reporte de defectos en GitLab.",
        "area": "QA", "seniority": "Junior", "experience_years": 1
    },


    {
        "text": "QA automation engineer using Selenium, Cypress and Playwright for end-to-end testing.",
        "area": "QA", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Ingeniero QA con 4 años. Automatización con Selenium WebDriver, Python, pytest. Pipelines CI/CD con GitHub Actions.",
        "area": "QA", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "QA engineer. Playwright, Cypress, Jest. API testing with Postman and RestAssured. Performance testing with JMeter.",
        "area": "QA", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": "QA automation mid. Framework de pruebas con Robot Framework, Selenium. Reportes con Allure. Integración con Jenkins.",
        "area": "QA", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "SDET engineer. Automated regression testing for SaaS platform. TypeScript, Playwright, GitHub Actions, test pyramid strategy.",
        "area": "QA", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "QA lead (mid). Coordinación del equipo de testing, definición de estrategias QA, automatización con Selenium y Python.",
        "area": "QA", "seniority": "Mid", "experience_years": 5
    },


    {
        "text": "Senior QA engineer with 8 years. Defined testing strategies, automated test frameworks, led quality processes for 5+ product teams.",
        "area": "QA", "seniority": "Senior", "experience_years": 8
    },
    {
        "text": "QA architect senior. Diseño de frameworks de automatización escalables. Selenium, Appium, Playwright, JMeter. Mentoring de equipos.",
        "area": "QA", "seniority": "Senior", "experience_years": 9
    },
    {
        "text": "Senior SDET. 8 years. Shifted left testing culture, contract testing with Pact, performance testing, chaos engineering.",
        "area": "QA", "seniority": "Senior", "experience_years": 8
    },


    {
        "text": "Estudiante de ciberseguridad. CTF competitions, Kali Linux básico, OWASP Top 10, análisis de vulnerabilidades web.",
        "area": "Seguridad", "seniority": "Junior", "experience_years": 0
    },
    {
        "text": "Junior security analyst. Vulnerability scanning with Nessus, OWASP testing, basic penetration testing on labs.",
        "area": "Seguridad", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Trainee SOC. Monitoreo de alertas en SIEM, clasificación de incidentes, análisis básico de logs de red.",
        "area": "Seguridad", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Ethical hacking enthusiast. Completed CEH coursework. Burp Suite, Kali Linux, SQL injection and XSS testing in CTFs.",
        "area": "Seguridad", "seniority": "Junior", "experience_years": 0
    },
    {
        "text": "Junior pentester. Pruebas de penetración en entornos controlados. Metasploit, Nmap, Wireshark, análisis de tráfico de red.",
        "area": "Seguridad", "seniority": "Junior", "experience_years": 1
    },


    {
        "text": "Cybersecurity analyst with experience in penetration testing, OWASP and Kali Linux. 4 years of experience.",
        "area": "Seguridad", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Analista de seguridad informática. Pentesting, análisis de malware, respuesta a incidentes, SIEM (Splunk), Linux.",
        "area": "Seguridad", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "SOC analyst. Threat hunting, SIEM management, malware analysis, incident response. 4 years in enterprise environments.",
        "area": "Seguridad", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Security engineer. Firewall management (Palo Alto, Fortinet), IDS/IPS, VPN administration, vulnerability management.",
        "area": "Seguridad", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Especialista en ciberseguridad. Auditorías de seguridad, pentesting web, análisis forense digital, gestión de cumplimiento ISO 27001.",
        "area": "Seguridad", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "Application security engineer. SAST, DAST tools integration in CI/CD. Code review for security vulnerabilities, OWASP training.",
        "area": "Seguridad", "seniority": "Mid", "experience_years": 4
    },


    {
        "text": "SOC analyst working with SIEM tools, malware analysis and incident response. 7 years of experience.",
        "area": "Seguridad", "seniority": "Senior", "experience_years": 7
    },
    {
        "text": "Senior penetration tester. Red team operations, exploit development, social engineering. OSCP certified. 8 years.",
        "area": "Seguridad", "seniority": "Senior", "experience_years": 8
    },
    {
        "text": "CISO adjunto. 10 años en ciberseguridad. Estrategia de seguridad, cumplimiento regulatorio, gestión de riesgos, SOC.",
        "area": "Seguridad", "seniority": "Senior", "experience_years": 10
    },
    {
        "text": "Senior cloud security architect. AWS security, IAM policies, GuardDuty, Security Hub, Zero Trust architecture.",
        "area": "Seguridad", "seniority": "Senior", "experience_years": 8
    },


    {
        "text": "Estudiante de diseño gráfico. Figma, Adobe XD, Photoshop, Illustrator. Proyectos de landing pages y branding universitario.",
        "area": "Diseño", "seniority": "Junior", "experience_years": 0
    },
    {
        "text": "Junior UI/UX designer. Wireframing and prototyping in Figma. User research basics, usability testing, design handoff to developers.",
        "area": "Diseño", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Diseñador junior. Figma, Adobe XD, Illustrator. Creación de mockups y prototipos para aplicaciones móviles y web.",
        "area": "Diseño", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Graphic design trainee. Adobe suite (Photoshop, Illustrator, InDesign), social media content design, basic Figma skills.",
        "area": "Diseño", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "UX designer in training. Completed Google UX Design Certificate. Figma prototypes, user journey maps, personas.",
        "area": "Diseño", "seniority": "Junior", "experience_years": 0
    },


    {
        "text": "UI/UX designer using Figma, wireframes and prototyping for responsive interfaces. 3 years of experience.",
        "area": "Diseño", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": "Diseñadora UI/UX mid-level. Figma, Sketch, sistemas de diseño, Design Tokens, colaboración con equipos de desarrollo.",
        "area": "Diseño", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Product designer. 4 years creating end-to-end product design. User research, IA, wireframing, Figma, Maze usability testing.",
        "area": "Diseño", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "UX researcher and designer. 3 años realizando entrevistas de usuario, pruebas de usabilidad, análisis de datos cualitativos.",
        "area": "Diseño", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": "Motion and UX designer. After Effects, Figma, Principle. Created interactive prototypes and microinteraction animations.",
        "area": "Diseño", "seniority": "Mid", "experience_years": 3
    },


    {
        "text": "Senior product designer with 8 years. Led design systems initiatives, mentored junior designers, collaborated with C-suite stakeholders.",
        "area": "Diseño", "seniority": "Senior", "experience_years": 8
    },
    {
        "text": "Head of design. 10 años liderando equipos de diseño. Design Systems, UX Strategy, branding corporativo, cultura de diseño.",
        "area": "Diseño", "seniority": "Senior", "experience_years": 10
    },
    {
        "text": "Senior UX architect. 9 years defining information architecture, design principles and accessibility standards for large platforms.",
        "area": "Diseño", "seniority": "Senior", "experience_years": 9
    },


    {
        "text": "Estudiante de desarrollo móvil. Android con Kotlin básico, proyectos universitarios de apps simples con Room y ViewModel.",
        "area": "Mobile", "seniority": "Junior", "experience_years": 0
    },
    {
        "text": "Junior React Native developer. Built simple mobile apps consuming REST APIs. Navigation with React Navigation, styling basics.",
        "area": "Mobile", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Flutter trainee. Dart básico, widgets, navegación, consumo de APIs REST. Proyecto de app de lista de tareas publicada en Google Play.",
        "area": "Mobile", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Junior iOS developer. Swift, SwiftUI basics. Built a personal finance app as capstone project at bootcamp.",
        "area": "Mobile", "seniority": "Junior", "experience_years": 1
    },


    {
        "text": "React Native developer. 4 years building cross-platform apps for iOS and Android. Redux, REST APIs, push notifications.",
        "area": "Mobile", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Desarrollador Android mid-level. Kotlin, Jetpack Compose, MVVM, Retrofit, Room, Coroutines. Apps publicadas en Google Play.",
        "area": "Mobile", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Flutter developer. 3 years. Dart, BLoC pattern, Firebase integration, custom animations, published on both stores.",
        "area": "Mobile", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": "iOS developer mid. Swift, UIKit, SwiftUI, Core Data, URLSession, MVVM. 4 years en startups de salud y fintech.",
        "area": "Mobile", "seniority": "Mid", "experience_years": 4
    },


    {
        "text": "Senior React Native engineer. 8 years mobile development. Native modules, performance optimization, CI/CD with Fastlane.",
        "area": "Mobile", "seniority": "Senior", "experience_years": 8
    },
    {
        "text": "Lead Android developer. 9 años. Kotlin, arquitectura modular, Hilt, Jetpack Compose. Liderazgo de equipo de 6 developers.",
        "area": "Mobile", "seniority": "Senior", "experience_years": 9
    },
    {
        "text": "Senior iOS architect. Swift, SwiftUI, Combine, TDD. Designed scalable modular iOS app architecture for enterprise banking app.",
        "area": "Mobile", "seniority": "Senior", "experience_years": 8
    },


    {
        "text": "Estudiante con conocimientos básicos de SQL. MySQL, consultas SELECT, JOIN, GROUP BY. Proyectos académicos con bases de datos relacionales.",
        "area": "Database", "seniority": "Junior", "experience_years": 0
    },
    {
        "text": "Junior DBA trainee. MySQL, PostgreSQL basics, backup procedures, simple query optimization.",
        "area": "Database", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Desarrollador junior con manejo de bases de datos. PostgreSQL, MySQL, consultas complejas, procedimientos almacenados básicos.",
        "area": "Database", "seniority": "Junior", "experience_years": 1
    },


    {
        "text": "Database administrator. PostgreSQL, MySQL, MongoDB. Query optimization, indexing, backup strategies, replication setup.",
        "area": "Database", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "DBA mid-level. Oracle, PostgreSQL. Tuning de queries, particionamiento de tablas, administración de backups, alta disponibilidad.",
        "area": "Database", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "Data engineer. PostgreSQL, BigQuery, Snowflake, dbt. Designed dimensional models and data warehouses for analytics.",
        "area": "Database", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "MongoDB specialist. Aggregation pipelines, sharding, replica sets, schema design patterns, Atlas cloud management.",
        "area": "Database", "seniority": "Mid", "experience_years": 3
    },


    {
        "text": "Senior DBA with 10 years. Oracle, PostgreSQL, MySQL. High availability, disaster recovery, performance tuning, capacity planning.",
        "area": "Database", "seniority": "Senior", "experience_years": 10
    },
    {
        "text": "Arquitecto de datos senior. 9 años. PostgreSQL, Oracle, Snowflake, Kafka. Diseño de arquitecturas de datos para sistemas críticos.",
        "area": "Database", "seniority": "Senior", "experience_years": 9
    },


    {
        "text": "Estudiante con interés en cloud. Cursando AWS Cloud Practitioner. EC2, S3, IAM básico en proyectos de laboratorio.",
        "area": "Cloud Computing", "seniority": "Junior", "experience_years": 0
    },
    {
        "text": "Junior cloud engineer. AWS fundamentals, basic Terraform, S3 bucket management, EC2 setup for dev environments.",
        "area": "Cloud Computing", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Trainee cloud. Azure fundamentals certificado. Desplegando VMs, App Services, Azure Functions básico.",
        "area": "Cloud Computing", "seniority": "Junior", "experience_years": 1
    },


    {
        "text": "AWS cloud engineer. EC2, RDS, Lambda, S3, CloudFormation, IAM. 4 years building and maintaining cloud infrastructure.",
        "area": "Cloud Computing", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Ingeniero cloud Azure. ARM Templates, Terraform, Azure DevOps, AKS, Azure Functions. 4 años en consultoría cloud.",
        "area": "Cloud Computing", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Multi-cloud engineer. AWS and GCP. Terraform, Kubernetes, cost optimization, auto-scaling, managed databases.",
        "area": "Cloud Computing", "seniority": "Mid", "experience_years": 4
    },


    {
        "text": "Senior cloud architect. AWS, Terraform, Kubernetes. Designed multi-region active-active architectures for fintech platforms.",
        "area": "Cloud Computing", "seniority": "Senior", "experience_years": 9
    },
    {
        "text": "Lead cloud engineer. 10 años. AWS Solutions Architect Professional. Lideré migraciones cloud de sistemas legacy en empresas enterprise.",
        "area": "Cloud Computing", "seniority": "Senior", "experience_years": 10
    },


    {
        "text": "Técnico de soporte nivel 1. Atención de tickets, soporte telefónico, resolución de incidencias de hardware y software.",
        "area": "Soporte Técnico", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "IT support technician. Help desk, ticketing with ServiceNow, hardware troubleshooting, Windows and Office 365 support.",
        "area": "Soporte Técnico", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Soporte técnico junior en call center. Diagnóstico de problemas de conectividad, soporte a usuarios finales, sistema de tickets.",
        "area": "Soporte Técnico", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Desktop support technician. Windows installation, Active Directory basics, printer setup, network connectivity troubleshooting.",
        "area": "Soporte Técnico", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Estudiante de sistemas trabajando en soporte universitario. Mantenimiento de PCs, instalación de software, soporte a docentes.",
        "area": "Soporte Técnico", "seniority": "Junior", "experience_years": 0
    },
    {
        "text": "Pasante en soporte TI. Gestión de inventario hardware, configuración de equipos nuevos, soporte nivel 1 presencial.",
        "area": "Soporte Técnico", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Junior IT support. Resolved hardware and software issues, managed user accounts in Active Directory, VPN setup.",
        "area": "Soporte Técnico", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Soporte técnico universitario. Mantenimiento de laboratorios de cómputo, instalación de software educativo, atención a estudiantes.",
        "area": "Soporte Técnico", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Entry-level IT technician. Remote desktop support, Outlook configuration, antivirus management, basic network troubleshooting.",
        "area": "Soporte Técnico", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Técnico PC freelance. Reparación de equipos, formateo, instalación de Windows, redes domésticas, recuperación de datos.",
        "area": "Soporte Técnico", "seniority": "Junior", "experience_years": 2
    },


    {
        "text": "IT support specialist. 4 years managing helpdesk, Active Directory, Group Policy, Exchange, SCCM deployments.",
        "area": "Soporte Técnico", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Especialista soporte TI. Soporte nivel 2, administración Active Directory, Office 365, gestión de incidentes críticos.",
        "area": "Soporte Técnico", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Senior helpdesk analyst. ITIL certified. Managed SLAs, escalation procedures, knowledge base, vendor coordination.",
        "area": "Soporte Técnico", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "IT field engineer. On-site support, network troubleshooting, server maintenance, backup verification, hardware upgrades.",
        "area": "Soporte Técnico", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Técnico TI senior. Soporte multinivel, administración de servidores Windows Server, Hyper-V, Active Directory, redes LAN/WAN.",
        "area": "Soporte Técnico", "seniority": "Mid", "experience_years": 5
    },


    {
        "text": "Técnico junior de infraestructura. Instalación de servidores físicos, cableado estructurado, mantenimiento de rack.",
        "area": "Infraestructura", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Junior infrastructure technician. VMware basics, Windows Server installation, server racking and stacking.",
        "area": "Infraestructura", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Trainee infraestructura. Linux básico, administración de VMs en VMware vSphere, monitoreo con Zabbix.",
        "area": "Infraestructura", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Estudiante de sistemas con interés en infraestructura. Laboratorios con Proxmox, VMs Linux, redes básicas, SSH.",
        "area": "Infraestructura", "seniority": "Junior", "experience_years": 0
    },
    {
        "text": "Junior sysadmin. Linux Ubuntu/CentOS administration, Apache/Nginx setup, user management, cron jobs, basic monitoring.",
        "area": "Infraestructura", "seniority": "Junior", "experience_years": 1
    },


    {
        "text": "Infrastructure engineer. VMware vSphere, Windows Server, Linux, SAN storage, backup (Veeam), monitoring Zabbix.",
        "area": "Infraestructura", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "Administrador de infraestructura. Virtualización con VMware y Proxmox, servidores Linux y Windows, almacenamiento NAS/SAN.",
        "area": "Infraestructura", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Systems administrator. Linux (RHEL, Ubuntu), Ansible automation, Nginx, HAProxy, monitoring with Grafana and Prometheus.",
        "area": "Infraestructura", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "Especialista en infraestructura on-premise. VMware vSphere, Windows Server 2019, Active Directory, DNS, DHCP, NPS.",
        "area": "Infraestructura", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Infrastructure and virtualization engineer. Proxmox cluster management, Ceph storage, LXC containers, pfSense firewalls.",
        "area": "Infraestructura", "seniority": "Mid", "experience_years": 4
    },


    {
        "text": "Senior infrastructure architect. 10 years. VMware, Nutanix HCI, NetApp SAN, DR planning, capacity planning.",
        "area": "Infraestructura", "seniority": "Senior", "experience_years": 10
    },
    {
        "text": "Arquitecto de infraestructura senior. Diseño de datacenters, virtualización VMware, redes Cisco, almacenamiento EMC.",
        "area": "Infraestructura", "seniority": "Senior", "experience_years": 11
    },
    {
        "text": "Lead infrastructure engineer. 9 years. Hybrid cloud (AWS + on-premise), Kubernetes, Terraform, Ansible. Team of 8.",
        "area": "Infraestructura", "seniority": "Senior", "experience_years": 9
    },


    {
        "text": "Junior sysadmin. Linux Ubuntu, administración básica de usuarios, permisos, cron, Nginx, firewall iptables.",
        "area": "SysAdmin", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Entry-level system administrator. Windows Server, Active Directory basics, Group Policy, file share management.",
        "area": "SysAdmin", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Estudiante sysadmin. Administración de sistemas Linux, scripts Bash, monitoreo con htop/netstat, SSH, crontab.",
        "area": "SysAdmin", "seniority": "Junior", "experience_years": 0
    },
    {
        "text": "Trainee administrador de sistemas. Windows Server 2019, Active Directory, backups, DNS, DHCP empresarial.",
        "area": "SysAdmin", "seniority": "Junior", "experience_years": 1
    },


    {
        "text": "Linux systems administrator. RHEL, CentOS, Ubuntu. Bash scripting automation, Ansible playbooks, Nginx, Apache, cron, monitoring.",
        "area": "SysAdmin", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "Administrador de sistemas Windows/Linux. Active Directory, Exchange, Office 365, Hyper-V, scripts PowerShell.",
        "area": "SysAdmin", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "SysAdmin mid-level. Ubuntu, Debian, RHEL. Docker, Nginx, Let's Encrypt, fail2ban, Zabbix monitoring, Ansible.",
        "area": "SysAdmin", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "System administrator. Windows Server, AD, Exchange, SCCM, Veeam backup. Managed infrastructure for 200+ users.",
        "area": "SysAdmin", "seniority": "Mid", "experience_years": 5
    },


    {
        "text": "Senior Linux sysadmin. 9 years. RHEL, Puppet, Chef, Ansible, Nagios, performance tuning, security hardening.",
        "area": "SysAdmin", "seniority": "Senior", "experience_years": 9
    },
    {
        "text": "Senior systems administrator. Windows y Linux. 10 años administrando infraestructura crítica. Hyper-V, VMware, AD, PKI.",
        "area": "SysAdmin", "seniority": "Senior", "experience_years": 10
    },
    {
        "text": "Lead sysadmin. Managed 500+ Linux servers. Puppet automation, Nagios/Prometheus monitoring, security hardening, DR procedures.",
        "area": "SysAdmin", "seniority": "Senior", "experience_years": 8
    },


    {
        "text": "Junior fullstack developer. React frontend, Node.js backend, PostgreSQL. Worked on freelance projects and bootcamp assignments.",
        "area": "Fullstack", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Desarrollador fullstack junior. Vue.js, Laravel, MySQL. Proyecto final académico: sistema de gestión de inventario.",
        "area": "Fullstack", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Trainee fullstack. React, Express, MongoDB. Built a simple task management app with user auth and CRUD operations.",
        "area": "Fullstack", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Egresado fullstack. Next.js, FastAPI, PostgreSQL. Portfolio de proyectos en GitHub. Buscando primer empleo.",
        "area": "Fullstack", "seniority": "Junior", "experience_years": 0
    },


    {
        "text": "Fullstack developer using React, Node.js, Express and PostgreSQL. Experience deploying applications on Linux servers.",
        "area": "Fullstack", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "Desarrollador fullstack mid. Angular + Spring Boot + PostgreSQL. 4 años en proyectos enterprise de gestión.",
        "area": "Fullstack", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Fullstack engineer. Next.js, Node.js, MongoDB, Docker. 4 years building SaaS applications end-to-end.",
        "area": "Fullstack", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Desarrollador fullstack. Vue.js + Django + PostgreSQL. Integración de pasarelas de pago, dashboards analíticos.",
        "area": "Fullstack", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": "Fullstack developer. React, TypeScript, Python FastAPI, PostgreSQL. Built internal tools for operations teams.",
        "area": "Fullstack", "seniority": "Mid", "experience_years": 4
    },


    {
        "text": "Senior fullstack engineer. 8 years. React, Node.js, PostgreSQL, Docker. Led 5-person team delivering SaaS platform.",
        "area": "Fullstack", "seniority": "Senior", "experience_years": 8
    },
    {
        "text": "Arquitecto fullstack senior. Vue.js, Nuxt, Laravel, MySQL, Redis. 10 años. Liderazgo técnico, definición de stack y arquitectura.",
        "area": "Fullstack", "seniority": "Senior", "experience_years": 10
    },
    {
        "text": "Senior fullstack developer. Next.js, Python Django, PostgreSQL, AWS. Designed and built multi-tenant SaaS from scratch.",
        "area": "Fullstack", "seniority": "Senior", "experience_years": 8
    },


    {
        "text": "Backend and DevOps engineer. Node.js REST APIs, Docker Compose, GitHub Actions CI/CD, Linux server administration. 4 years.",
        "area": "Backend", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Desarrollador backend con experiencia en DevOps. Python FastAPI, Docker, Kubernetes, AWS. Deploy automatizado con Terraform.",
        "area": "Backend", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "Backend engineer transitioning to DevOps. Node.js, Express, Docker, Linux, CI/CD pipelines, basic Terraform.",
        "area": "Backend", "seniority": "Mid", "experience_years": 4
    },

    {
        "text": "Frontend developer with strong design skills. React, Figma, TailwindCSS. Implements pixel-perfect UI from design specs.",
        "area": "Frontend", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": "Diseñador y desarrollador frontend. Figma, HTML, CSS, Vue.js. Proyecto de diseño end-to-end: wireframes hasta implementación.",
        "area": "Frontend", "seniority": "Mid", "experience_years": 4
    },

    {
        "text": "Network and Linux administrator. Cisco routing, switching, DNS, DHCP, Linux server administration, SSH, Bash scripting.",
        "area": "Networking", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "Técnico de redes y sistemas Linux. Mikrotik, VLANs, Ubuntu Server, Nginx, SSH, monitoreo con Zabbix.",
        "area": "Networking", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Network engineer with Linux expertise. Cisco IOS, pfSense, Ubuntu Server, Bash scripts, DNS/DHCP management.",
        "area": "Networking", "seniority": "Mid", "experience_years": 4
    },

    {
        "text": "Backend developer with AWS cloud experience. Node.js, Lambda, API Gateway, RDS, Docker, S3. Serverless architectures.",
        "area": "Backend", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Python backend engineer con experiencia en cloud. FastAPI, AWS Lambda, DynamoDB, SQS, Docker. Arquitecturas serverless.",
        "area": "Backend", "seniority": "Mid", "experience_years": 4
    },

    {
        "text": "DevOps and sysadmin engineer. Linux, Ansible, Docker, Nginx, monitoring, CI/CD. Migrated bare-metal to containerized infra.",
        "area": "DevOps", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "SysAdmin devenido DevOps. Administración Linux, Docker, GitHub Actions, Terraform, Grafana, Prometheus. 5 años.",
        "area": "DevOps", "seniority": "Mid", "experience_years": 5
    },

    {
        "text": "IT support specialist with infrastructure knowledge. Helpdesk, Active Directory, VMware VMs, network troubleshooting.",
        "area": "Soporte Técnico", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Soporte técnico avanzado con experiencia en infraestructura. Windows Server, Linux, VMware, backups, networking básico.",
        "area": "Soporte Técnico", "seniority": "Mid", "experience_years": 4
    },

    {
        "text": "Fullstack developer with DevOps skills. React, Node.js, PostgreSQL, Docker, GitHub Actions, AWS. Self-sufficient for deployments.",
        "area": "Fullstack", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "Desarrollador fullstack y DevOps. Vue.js, FastAPI, Docker Compose, CI/CD con GitLab, despliegues en VPS Linux.",
        "area": "Fullstack", "seniority": "Mid", "experience_years": 4
    },

    {
        "text": "Network and infrastructure engineer. Cisco Catalyst, VMware, DNS, DHCP, firewall Fortinet, Zabbix monitoring.",
        "area": "Networking", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "Ingeniero de redes e infraestructura. Cisco, Mikrotik, VMware vSphere, Windows Server, Linux, cableado estructurado.",
        "area": "Infraestructura", "seniority": "Mid", "experience_years": 5
    },

    {
        "text": "ML engineer with backend experience. Python, FastAPI, scikit-learn, Docker. Built and deployed ML models as REST APIs.",
        "area": "Data Science", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Data scientist con backend. Python, Django, pandas, PostgreSQL, scikit-learn. Pipeline de datos end-to-end.",
        "area": "Data Science", "seniority": "Mid", "experience_years": 4
    },


    {
        "text": "Estudiante de Ingeniería en Sistemas. Experiencia en Node.js, Express, EJS, JavaScript, Linux y servidores SSH. Conocimientos de redes, CCNA, soporte técnico e infraestructura.",
        "area": "Backend", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Computer science student. Passionate about backend development and cloud computing. Projects with Python, Flask, AWS free tier.",
        "area": "Backend", "seniority": "Junior", "experience_years": 0
    },
    {
        "text": "Estudiante de telecomunicaciones. Conocimientos en redes, CCNA en curso, Linux, soporte técnico universitario.",
        "area": "Networking", "seniority": "Junior", "experience_years": 0
    },
    {
        "text": "Egresado reciente en Ciencias de Datos. Python, pandas, matplotlib, SQL. Tesis sobre modelos de clasificación.",
        "area": "Data Science", "seniority": "Junior", "experience_years": 0
    },
    {
        "text": "IT student working part-time as helpdesk support. Ticketing, hardware troubleshooting, basic networking.",
        "area": "Soporte Técnico", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Estudiante de diseño multimedia. Figma, Adobe XD, Illustrator. Proyectos de UI para apps móviles y sitios web.",
        "area": "Diseño", "seniority": "Junior", "experience_years": 0
    },
    {
        "text": "Trainee QA. Probando aplicaciones web manualmente, aprendiendo Selenium, documentando casos de prueba en Confluence.",
        "area": "QA", "seniority": "Junior", "experience_years": 0
    },
    {
        "text": "Apprentice DevOps. Running Linux VMs in VirtualBox, writing basic Bash scripts, learning Docker from online courses.",
        "area": "DevOps", "seniority": "Junior", "experience_years": 0
    },
    {
        "text": "Android development student. Kotlin, basic Jetpack libraries. Published simple calculator app on Play Store as learning exercise.",
        "area": "Mobile", "seniority": "Junior", "experience_years": 0
    },
    {
        "text": "Estudiante de ciberseguridad. CTFs en HackTheBox, Kali Linux, conceptos de OWASP. Aprendiendo pentesting ético.",
        "area": "Seguridad", "seniority": "Junior", "experience_years": 0
    },


    {
        "text": """
EXPERIENCIA LABORAL

Desarrollador Backend - Empresa TechSoft S.A.
Enero 2022 - Actualidad

- Desarrollo de APIs REST con Node.js y Express
- Gestión de base de datos PostgreSQL
- Implementación de autenticación JWT
- Despliegue en servidor Linux con Nginx
- Integración con servicios de terceros (Stripe, SendGrid)

HABILIDADES: Node.js, Express, PostgreSQL, JWT, Linux, Nginx, Git
""",
        "area": "Backend", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": """
PERFIL PROFESIONAL

Ingeniero de Redes con 6 años de experiencia en administración de infraestructura
de telecomunicaciones. Especialista en equipos Cisco y Mikrotik.

EXPERIENCIA

Administrador de Red - ISP Regional
2019 - 2025

- Gestión de routers Cisco (IOS) y Mikrotik (RouterOS)
- Configuración de VLANs, OSPF y BGP
- Administración de firewall pfSense
- Monitoreo de red con Zabbix y MRTG
- Soporte de conectividad para +2000 clientes
""",
        "area": "Networking", "seniority": "Mid", "experience_years": 6
    },
    {
        "text": """
Técnico de Soporte - Universidad Nacional
Marzo 2021 - Actualidad

Responsable del laboratorio de cómputo.

Funciones:
- Mantenimiento preventivo y correctivo de 80 equipos
- Instalación y configuración de software académico
- Soporte a docentes y estudiantes
- Administración de red LAN del laboratorio
- Gestión de inventario de hardware

Habilidades: Windows 10/11, Linux Ubuntu, redes LAN, cableado estructurado
""",
        "area": "Soporte Técnico", "seniority": "Junior", "experience_years": 4
    },
    {
        "text": """
INGENIERO DEVOPS

EXPERIENCIA:

Senior DevOps Engineer - FinTech Global
2020 - 2025 (5 años)

Logros:
- Migré arquitectura monolítica a microservicios en Kubernetes
- Reduje tiempos de deploy de 2 horas a 8 minutos con GitHub Actions
- Implementé observabilidad completa con Prometheus, Grafana y Jaeger
- Gestioné infraestructura AWS: EKS, RDS, ElastiCache, S3

Stack: Docker, Kubernetes, Terraform, AWS, GitHub Actions, Helm, Prometheus, Grafana
""",
        "area": "DevOps", "seniority": "Senior", "experience_years": 5
    },
    {
        "text": """
ANALISTA QA - CV

Perfil: Analista de QA con 3 años de experiencia en testing manual y automatizado.

Proyectos:
- Automatización de pruebas E2E con Cypress para plataforma SaaS
- API testing con Postman y Newman en CI/CD
- Performance testing con JMeter para sistema de pagos

Tecnologías: Cypress, Selenium, Python, pytest, Postman, Jira, Confluence, GitHub Actions
""",
        "area": "QA", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": """
CV - Desarrollador Frontend

Nombre: Carlos M.

Sobre mí: Desarrollador frontend apasionado por crear interfaces intuitivas y de alto rendimiento.

Experiencia:
2022-2025 | Frontend Developer | Agencia Digital CreaTech
- Desarrollo de aplicaciones SPA con React y TypeScript
- Implementación de Design System con Storybook y TailwindCSS
- Optimización de rendimiento (Lighthouse 95+ en todos los proyectos)
- Colaboración con diseñadores UX y backend developers

Stack: React, TypeScript, Next.js, TailwindCSS, Redux Toolkit, Git
""",
        "area": "Frontend", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": """
Perfil Profesional - Administrador de Sistemas

7 años gestionando infraestructura tecnológica en empresa manufacturera.

Área de expertise:
- Virtualización: VMware vSphere 7, vCenter, Hyper-V
- Sistemas operativos: Windows Server 2019, RHEL 8, Ubuntu 22
- Directorio Activo, DNS, DHCP, PKI corporativa
- Backup y recuperación: Veeam Backup & Replication
- Monitoreo: PRTG Network Monitor, Zabbix
- Almacenamiento: NetApp ONTAP, Dell EMC Unity
""",
        "area": "SysAdmin", "seniority": "Senior", "experience_years": 7
    },
    {
        "text": """
CURRICULUM VITAE

Especialista en Ciberseguridad

Certificaciones: CEH, CompTIA Security+, OSCP (en proceso)

Experiencia actual:
SOC Analyst - Banco Nacional (2021-2025)

- Monitoreo de alertas en SIEM Splunk
- Análisis forense de incidentes
- Threat hunting proactivo
- Gestión de vulnerabilidades con Tenable Nessus
- Respuesta a incidentes de seguridad

Herramientas: Splunk, Wireshark, Kali Linux, Metasploit, Burp Suite, Nessus
""",
        "area": "Seguridad", "seniority": "Mid", "experience_years": 4
    },


    {
        "text": """
MACHINE LEARNING ENGINEER

WORK EXPERIENCE

Senior ML Engineer | DataTech Inc. | 2019 - 2025

- Designed and deployed recommendation systems serving 10M+ daily users
- Built NLP pipelines for document classification using scikit-learn and spaCy
- Orchestrated ML workflows with Apache Airflow and MLflow
- Collaborated with data engineers on feature stores using Feast
- Mentored 3 junior data scientists

Tech Stack: Python, scikit-learn, TensorFlow, Spark, Kafka, Airflow, MLflow, PostgreSQL
""",
        "area": "Data Science", "seniority": "Senior", "experience_years": 6
    },
    {
        "text": """
FULL STACK DEVELOPER - RESUME

Summary: Experienced full stack developer with 5 years building scalable web applications
for startups and SMBs.

Experience:
Lead Developer | GrowthApp | 2021 - 2025
- Architected React + Node.js SaaS platform from 0 to 50K users
- Designed PostgreSQL schema, optimized queries, implemented caching with Redis
- Set up Docker + GitHub Actions CI/CD pipeline
- Integrated Stripe payments and Twilio SMS

Skills: React, TypeScript, Node.js, Express, PostgreSQL, Redis, Docker, AWS, Git
""",
        "area": "Fullstack", "seniority": "Senior", "experience_years": 5
    },
    {
        "text": """
NETWORK ENGINEER - CV

Profile: Certified network professional (CCNP) with 7 years managing enterprise networks.

Experience:
Senior Network Engineer | TeleCorp | 2018 - 2025

- Designed and implemented BGP routing for 3 data centers
- Managed Cisco Catalyst switching infrastructure (200+ switches)
- Deployed SD-WAN solution across 15 branch offices
- Led Fortinet firewall migration project
- Mentored junior network technicians

Certifications: CCNP Enterprise, Fortinet NSE 4, CompTIA Network+
""",
        "area": "Networking", "seniority": "Senior", "experience_years": 7
    },


    {
        "text": "Backend developer. 3 años trabajando con Node.js, REST APIs y PostgreSQL. Experience with Docker y Linux servers. Ganas de crecer en arquitecturas cloud.",
        "area": "Backend", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": "Frontend engineer con experiencia en React y TypeScript. Worked on responsive interfaces, state management with Redux, and API integration.",
        "area": "Frontend", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": "Desarrollador Python. Machine learning projects with scikit-learn y pandas. Experiencia en análisis de datos y creación de modelos predictivos.",
        "area": "Data Science", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": "Network administrator. Administración de redes Cisco y Mikrotik. Experience configuring VLANs, routing protocols, y firewall rules.",
        "area": "Networking", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "DevOps engineer. Trabajo con Docker, Kubernetes y pipelines CI/CD. Experience in AWS infrastructure y Terraform automation.",
        "area": "DevOps", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "QA analyst. Testing manual y automatizado con Cypress. Experience writing test plans, bug reporting y API testing con Postman.",
        "area": "QA", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": "Ciberseguridad. Penetration testing con Kali Linux. Experience in OWASP vulnerabilities, SIEM monitoring y incident response.",
        "area": "Seguridad", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Administrador de sistemas. Linux y Windows Server management. Experiencia con Ansible automation, Nginx, y monitoring with Zabbix.",
        "area": "SysAdmin", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Flutter developer. Apps cross-platform para iOS y Android. Experience with BLoC pattern, REST API integration y Firebase.",
        "area": "Mobile", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": "Diseñadora UX/UI. Figma wireframes y prototypes. Experience conducting user interviews, usability testing y creación de design systems.",
        "area": "Diseño", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": "Soporte técnico nivel 2. IT helpdesk con Active Directory y Office 365. Experiencia en troubleshooting de red y administración de equipos.",
        "area": "Soporte Técnico", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": "Infrastructure engineer. Virtualización con VMware vSphere. Experiencia en Linux server management, storage administration y Veeam backups.",
        "area": "Infraestructura", "seniority": "Mid", "experience_years": 4
    },


    {
        "text": """
- Node.js REST API development
- PostgreSQL database design and optimization
- JWT authentication implementation
- Docker containerization
- Linux server deployment with Nginx
- Redis caching integration
""",
        "area": "Backend", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": """
- React y TypeScript frontend development
- Consumo de APIs REST
- Manejo de estado con Redux Toolkit
- Testing con Jest y React Testing Library
- Diseño responsivo con TailwindCSS
- Deploy en Vercel y Netlify
""",
        "area": "Frontend", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": """
- Docker y Docker Compose para ambientes de desarrollo y producción
- Kubernetes cluster administration
- Terraform infrastructure as code
- GitHub Actions CI/CD pipelines
- AWS EC2, S3, RDS management
- Monitoreo con Prometheus y Grafana
""",
        "area": "DevOps", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": """
- Cisco router and switch configuration
- VLAN design and implementation
- OSPF and BGP routing protocols
- Mikrotik RouterOS administration
- Firewall management (pfSense, Fortinet)
- Network monitoring with Zabbix and MRTG
""",
        "area": "Networking", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": """
- Python pandas para limpieza y análisis de datos
- Modelos de clasificación con scikit-learn
- Visualizaciones con matplotlib y seaborn
- SQL para extracción de datos
- Reportes en Jupyter Notebooks
- Deploy de modelos con FastAPI
""",
        "area": "Data Science", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": """
- Automated E2E tests with Cypress
- API testing with Postman and Newman
- Performance testing with JMeter
- Bug tracking in Jira
- CI/CD pipeline integration for tests
- Test documentation in Confluence
""",
        "area": "QA", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": """
- Resolución de tickets nivel 1 y 2
- Administración Active Directory
- Soporte Office 365 y Teams
- Mantenimiento hardware PCs y laptops
- Configuración de redes LAN
- Inventario y control de equipos
""",
        "area": "Soporte Técnico", "seniority": "Junior", "experience_years": 2
    },
    {
        "text": """
- VMware vSphere virtualization management
- Windows Server 2019 administration
- Active Directory, DNS, DHCP
- Veeam backup and recovery
- SAN storage administration
- Linux server management
""",
        "area": "Infraestructura", "seniority": "Mid", "experience_years": 5
    },


    {
        "text": "CTO de startup fintech. 12 años en desarrollo de software. Lideré equipos de hasta 20 personas. Stack: React, Node.js, Python, PostgreSQL, AWS, Kubernetes.",
        "area": "Backend", "seniority": "Senior", "experience_years": 12
    },
    {
        "text": "VP of Engineering. 15 years in software development. Led full stack teams building SaaS products. React, Node.js, Python, AWS, Terraform.",
        "area": "Fullstack", "seniority": "Senior", "experience_years": 15
    },
    {
        "text": "Director de infraestructura. 13 años gestionando centros de datos y equipos de SysAdmins. VMware, Cisco, AWS, Azure, gestión de presupuesto TI.",
        "area": "Infraestructura", "seniority": "Senior", "experience_years": 13
    },
    {
        "text": "Head of Security. CISO function at mid-size enterprise. 11 years. Designed security architecture, managed compliance, built SOC from scratch.",
        "area": "Seguridad", "seniority": "Senior", "experience_years": 11
    },
    {
        "text": "Network operations manager. 10 años. Gestión de equipo de 15 ingenieros de red. Cisco, Juniper, SD-WAN, NOC 24/7.",
        "area": "Networking", "seniority": "Senior", "experience_years": 10
    },


    {
        "text": "Freelance backend developer. Builds REST APIs for SMBs. Node.js, Express, PostgreSQL, MongoDB. Remote work, project-based.",
        "area": "Backend", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Desarrolladora frontend freelance. React, Tailwind, WordPress. Clientes de Argentina, México y Colombia. Proyectos de e-commerce y portfolios.",
        "area": "Frontend", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Consultor redes freelance. Diseño e implementación de redes Cisco y Mikrotik para pymes. VLAN, VPN, wireless.",
        "area": "Networking", "seniority": "Mid", "experience_years": 6
    },
    {
        "text": "Data science consultant. Freelance projects in predictive analytics, NLP, reporting dashboards. Python, R, Power BI.",
        "area": "Data Science", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "Diseñadora UX freelance. Figma, Sketch, Adobe XD. Proyectos para startups y agencias. Portfolios, apps móviles y dashboards.",
        "area": "Diseño", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Freelance DevOps consultant. Helps startups set up Docker, GitHub Actions, AWS infrastructure. Terraform, Nginx, monitoring.",
        "area": "DevOps", "seniority": "Mid", "experience_years": 5
    },


    {
        "text": "Java backend developer in banking sector. Spring Boot, Oracle DB, Kafka, SOAP/REST services, IBM MQ. 6 years in financial systems.",
        "area": "Backend", "seniority": "Mid", "experience_years": 6
    },
    {
        "text": "Analista de seguridad informática en banco. SIEM, PCI-DSS compliance, gestión de vulnerabilidades, análisis forense. 5 años.",
        "area": "Seguridad", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "DBA Oracle en empresa financiera. Tuning de queries críticas, particionamiento, RAC, Data Guard, respaldo RMAN.",
        "area": "Database", "seniority": "Senior", "experience_years": 9
    },
    {
        "text": "Enterprise network engineer. Cisco ACI, MPLS backbone, datacenter networking, BGP policy design. 8 years in banking.",
        "area": "Networking", "seniority": "Senior", "experience_years": 8
    },


    {
        "text": "Node.js developer. REST APIs, PostgreSQL, Docker. 3 years experience. Looking for backend opportunities.",
        "area": "Backend", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": "React developer. TypeScript, TailwindCSS, Next.js. 4 años. Open to remote positions.",
        "area": "Frontend", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "CCNA certificado. Cisco, Mikrotik, VLANs, firewall, DNS. 3 años en soporte de redes empresariales.",
        "area": "Networking", "seniority": "Junior", "experience_years": 3
    },
    {
        "text": "Python developer with ML experience. scikit-learn, pandas, FastAPI. 4 years.",
        "area": "Data Science", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "DevOps. Docker, Kubernetes, AWS, Terraform, GitHub Actions. 5 years in cloud infrastructure.",
        "area": "DevOps", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "QA automation. Cypress, Playwright, Python. CI/CD integration. 3 years.",
        "area": "QA", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": "Pentester. Kali Linux, Burp Suite, OWASP, Metasploit. CEH certificado. 4 años.",
        "area": "Seguridad", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "UI/UX designer. Figma, wireframes, user testing, design systems. 4 years in product design.",
        "area": "Diseño", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "React Native developer. iOS y Android. 3 años. Firebase, REST APIs, Redux.",
        "area": "Mobile", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": "Linux sysadmin. Ubuntu, RHEL, Ansible, Nginx, monitoring, scripting Bash. 5 años.",
        "area": "SysAdmin", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "Técnico soporte TI. Windows, Active Directory, Office 365, helpdesk, networking básico. 2 años.",
        "area": "Soporte Técnico", "seniority": "Junior", "experience_years": 2
    },
    {
        "text": "Infrastructure engineer. VMware, Windows Server, Linux, Veeam, SAN. 5 años en datacenter.",
        "area": "Infraestructura", "seniority": "Mid", "experience_years": 5
    },


    {
        "text": "I am a backend developer with 5 years of experience designing and maintaining REST APIs using Node.js and Python. I have deep knowledge of PostgreSQL, Redis, and microservices architecture. I enjoy building scalable systems and collaborating with cross-functional teams.",
        "area": "Backend", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "Soy un desarrollador frontend apasionado por crear experiencias de usuario excepcionales. Llevo 4 años trabajando con React, TypeScript y TailwindCSS. Me especializo en optimización de performance y accesibilidad web.",
        "area": "Frontend", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "As a DevOps engineer with 6 years of experience, I specialize in cloud infrastructure on AWS and GCP. I have extensive experience with Kubernetes, Terraform, and CI/CD pipeline design. I am passionate about automation and reliability engineering.",
        "area": "DevOps", "seniority": "Senior", "experience_years": 6
    },
    {
        "text": "Soy técnico de redes con certificación CCNA y 4 años administrando infraestructura Cisco y Mikrotik. Me especializo en diseño de VLANs, routing y troubleshooting de conectividad en entornos empresariales.",
        "area": "Networking", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "I am a data scientist with a strong background in machine learning and NLP. I have 5 years of experience building predictive models with scikit-learn, XGBoost, and PyTorch. I am particularly interested in applied AI for business problems.",
        "area": "Data Science", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "Como analista QA con 3 años de experiencia, domino tanto el testing manual como la automatización con Cypress y Selenium. Tengo experiencia trabajando en equipos ágiles y soy defensor de las buenas prácticas de calidad de software.",
        "area": "QA", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": "I am a cybersecurity professional with 5 years of experience in penetration testing, vulnerability assessment, and incident response. I hold CEH and Security+ certifications. I am passionate about protecting critical business systems.",
        "area": "Seguridad", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "Soy diseñadora UX/UI con 4 años creando productos digitales centrados en el usuario. Me especializo en investigación de usuarios, arquitectura de información y prototipado en Figma. Creo que el buen diseño debe ser tanto funcional como estético.",
        "area": "Diseño", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "As a mobile developer with 4 years of experience, I build cross-platform applications with Flutter and React Native. I have published 6 apps on both the App Store and Google Play. I care deeply about performance and user experience on mobile devices.",
        "area": "Mobile", "seniority": "Mid", "experience_years": 4
    },
    {
        "text": "Soy administrador de sistemas con 6 años gestionando infraestructura Linux y Windows Server. Me especializo en virtualización VMware, automatización con Ansible y monitoreo con Zabbix. Disfruto optimizar sistemas y garantizar su disponibilidad 24/7.",
        "area": "SysAdmin", "seniority": "Senior", "experience_years": 6
    },


    {
        "text": "Backend developer Node.js con 2 años. APIs REST, Express, MongoDB, Docker básico. Primer empleo formal en startup tecnológica.",
        "area": "Backend", "seniority": "Junior", "experience_years": 2
    },
    {
        "text": "Cloud architect AWS. 8 años. Multi-account strategies, Landing Zone, Service Control Policies, Well-Architected reviews.",
        "area": "Cloud Computing", "seniority": "Senior", "experience_years": 8
    },
    {
        "text": "Desarrollador Kotlin Android. 3 años. MVVM, Retrofit, Room, Hilt, Coroutines, Jetpack Compose. Apps de salud y productividad.",
        "area": "Mobile", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": "Senior QA automation. 8 años. Framework design con Selenium + Java, Cucumber BDD, liderazgo de equipos de testing.",
        "area": "QA", "seniority": "Senior", "experience_years": 8
    },
    {
        "text": "Junior cloud engineer. GCP fundamentals, Compute Engine, Cloud Storage, BigQuery. Aprendiendo Terraform y Kubernetes.",
        "area": "Cloud Computing", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Fullstack Ruby on Rails developer. 5 años. PostgreSQL, Sidekiq, RSpec, React frontend, Heroku y AWS. SaaS para pymes.",
        "area": "Fullstack", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "Penetration tester senior. OSCP. Red team operations, custom exploit development, social engineering, phishing simulations.",
        "area": "Seguridad", "seniority": "Senior", "experience_years": 9
    },
    {
        "text": "Data engineer. Apache Spark, Kafka, Airflow, dbt, Snowflake. Pipelines ETL a escala de terabytes diarios.",
        "area": "Data Science", "seniority": "Senior", "experience_years": 7
    },
    {
        "text": "Network security engineer. Palo Alto NGFW, Cisco ASA, IDS/IPS management, NAC, zero trust network access.",
        "area": "Seguridad", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "Diseñador gráfico y UX senior. 10 años. Branding corporativo, Design Systems, Figma, motion design, liderazgo creativo.",
        "area": "Diseño", "seniority": "Senior", "experience_years": 10
    },
    {
        "text": "Junior data scientist. Modelos de regresión y clasificación con scikit-learn. Visualización en matplotlib. SQL, pandas, numpy.",
        "area": "Data Science", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "iOS developer senior. Swift, UIKit, SwiftUI, Core Data, CloudKit. 9 años publicando apps en App Store.",
        "area": "Mobile", "seniority": "Senior", "experience_years": 9
    },
    {
        "text": "Administrador de base de datos PostgreSQL. Replicación streaming, particionamiento, tuning de queries, PgBouncer, Patroni HA.",
        "area": "Database", "seniority": "Mid", "experience_years": 5
    },
    {
        "text": "Junior sysadmin. Ubuntu Server 22.04, Nginx, Let's Encrypt, Fail2ban, Netplan, cron. Primer trabajo en hosting provider.",
        "area": "SysAdmin", "seniority": "Junior", "experience_years": 1
    },
    {
        "text": "Senior infrastructure engineer. Nutanix AHV, VMware vSAN, Cisco UCS, NetApp. Designed hyper-converged datacenter.",
        "area": "Infraestructura", "seniority": "Senior", "experience_years": 10
    },
    {
        "text": "Especialista soporte técnico nivel 3. Escalaciones complejas, administración Windows Server, troubleshooting avanzado, documentación técnica.",
        "area": "Soporte Técnico", "seniority": "Senior", "experience_years": 7
    },
    {
        "text": "Mid backend developer. Python Django, PostgreSQL, Celery, Redis, Docker. SaaS de gestión de proyectos. 3 años.",
        "area": "Backend", "seniority": "Mid", "experience_years": 3
    },
    {
        "text": "CCNP Enterprise certified network engineer. BGP, MPLS, SD-WAN, wireless Cisco, network automation with Python.",
        "area": "Networking", "seniority": "Senior", "experience_years": 7
    },
    {
        "text": "Vue.js developer. 2 años. Vuex, Vue Router, Vite, Axios, TailwindCSS. Primer trabajo en empresa de e-learning.",
        "area": "Frontend", "seniority": "Junior", "experience_years": 2
    },
    {
        "text": "Arquitecto DevOps senior. GitOps, ArgoCD, Crossplane, Kubernetes multi-cluster, Terraform Cloud, política as code con OPA.",
        "area": "DevOps", "seniority": "Senior", "experience_years": 10
    },
]

df = pd.DataFrame(data)

os.makedirs("datasets", exist_ok=True)

df.to_csv("datasets/cv_data.csv", index=False)

print(f"Dataset creado: {len(df)} registros")
print("\nDistribución por área:")
print(df["area"].value_counts())
print("\nDistribución por seniority:")
print(df["seniority"].value_counts())
print("\nDistribución por área y seniority:")
print(df.groupby(["area", "seniority"]).size().to_string())