
"""
Advanced Python & Production Engineering Roadmap
================================================

Creates a structured learning directory for:
- Professional Python
- Production-grade backend engineering
- FastAPI and REST APIs
- Database engineering and data integration
- Asynchronous and distributed systems
- Security, testing, deployment, and observability
- Scientific computing, computational biology, and drug discovery
- Industry-oriented capstone projects

Design principles:
- Idempotent: safe to run repeatedly.
- Non-destructive: never overwrites existing files.
- Extensible: add topics by editing ROADMAP.
- pathlib-based filesystem operations.
- Preserves the original roadmap's learning workflow.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


ROOT_FOLDER = Path("Advanced Python")


ROADMAP: dict[str, Any] = {
    # =========================================================
    # 01. PROFESSIONAL PYTHON
    # =========================================================
    "01_Professional_Python": [
        "01_Type_Hints",
        "02_Mypy",
        "03_Ruff",
        "04_Black",
        "05_isort",
        "06_Pre_commit",
        "07_Logging",
        "08_Structured_Logging",
        "09_Config_Management",
        "10_Environment_Variables",
        "11_Context_Managers",
        "12_Descriptors",
        "13_Metaclasses",
        "14_Advanced_Generators",
        "15_Iterators_and_Iterables",
        "16_Decorators_and_Closures",
        "17_Memory_Management",
        "18_Garbage_Collection",
        "19_Profiling",
        "20_Debugging",
        "21_Exceptions_and_Error_Handling",
        "22_Packaging",
        "23_Dependency_Management",
        "24_Virtual_Environments",
        "25_Publishing",
        "26_Python_Internals",
        "27_CPython_Overview",
        "28_Protocols_and_Generics",
        "29_Dataclasses_and_NamedTuples",
        "30_Standard_Library_Essentials",
    ],

    # =========================================================
    # 02. ADVANCED BACKEND DEVELOPMENT
    # =========================================================
    "02_Advanced_Backend_Development": [
        "01_Backend_Architecture",
        "02_Layered_Architecture",
        "03_Clean_Architecture",
        "04_Hexagonal_Architecture",
        "05_Domain_Driven_Design",
        "06_Service_Layer",
        "07_Repository_Pattern",
        "08_Dependency_Injection",
        "09_API_Architecture",
        "10_Project_Structure",
        "11_Application_Lifecycle",
        "12_Separation_of_Concerns",
        "13_Domain_Models_and_Schemas",
        "14_Error_Handling_Strategy",
        "15_Configuration_by_Environment",
        "16_Application_Factory_Pattern",
    ],

    # =========================================================
    # 03. REST API DEVELOPMENT
    # =========================================================
    "03_REST_API_Development": [
        "01_HTTP",
        "02_Request_Response_Lifecycle",
        "03_REST_Principles",
        "04_API_Design",
        "05_OpenAPI",
        "06_Swagger",
        "07_JSON",
        "08_XML",
        "09_API_Versioning",
        "10_Status_Codes",
        "11_Error_Response_Standards",
        "12_Pagination",
        "13_Filtering_and_Sorting",
        "14_Rate_Limiting",
        "15_Idempotency",
        "16_Timeouts_and_Retries",
        "17_Caching_and_HTTP_Headers",
        "18_API_Testing",
        "19_Postman",
        "20_HTTPX",
        "21_Requests",
        "22_Webhooks",
        "23_File_Transfer",
        "24_API_Documentation",
    ],

    # =========================================================
    # 04. FASTAPI PROFESSIONAL
    # =========================================================
    "04_FastAPI_Professional": [
        "01_FastAPI_Basics",
        "02_Routers",
        "03_Dependency_Injection",
        "04_Pydantic",
        "05_Request_Validation",
        "06_Response_Models",
        "07_Application_Lifecycle",
        "08_Configuration_and_Settings",
        "09_File_Uploads",
        "10_Background_Tasks",
        "11_WebSockets",
        "12_Middleware",
        "13_CORS",
        "14_Authentication",
        "15_Authorization",
        "16_JWT",
        "17_OAuth2",
        "18_FastAPI_Security",
        "19_Global_Exception_Handlers",
        "20_Database_Integration",
        "21_Async_Database_Access",
        "22_Testing_FastAPI",
        "23_Health_and_Readiness_Endpoints",
        "24_Graceful_Shutdown",
        "25_Production_Deployment",
    ],

    # =========================================================
    # 05. DATABASE ENGINEERING
    # =========================================================
    "05_Database_Engineering": [
        "01_SQL",
        "02_PostgreSQL",
        "03_SQLAlchemy",
        "04_SQLModel",
        "05_Alembic",
        "06_ORM",
        "07_CRUD",
        "08_Relationships_and_Constraints",
        "09_Indexes",
        "10_Transactions",
        "11_Transaction_Isolation",
        "12_Connection_Pooling",
        "13_Query_Optimization",
        "14_Explain_and_Analyze",
        "15_Database_Design",
        "16_Normalization",
        "17_Views",
        "18_Stored_Procedures",
        "19_Concurrency_Control",
        "20_Deadlocks",
        "21_Optimistic_and_Pessimistic_Locking",
        "22_Migration_Strategy",
        "23_Database_Backups",
        "24_Restore_and_Recovery",
        "25_Database_Security",
        "26_Testing_Database_Code",
        "27_Test_Databases_and_Fixtures",
        "28_Connection_Failure_Handling",
    ],

    # =========================================================
    # 06. DATA INTEGRATION AND ETL
    # =========================================================
    "06_Data_Integration_ETL": [
        "01_ETL",
        "02_ELT",
        "03_Data_Validation",
        "04_Data_Cleaning",
        "05_API_Data_Integration",
        "06_SQL_Integration",
        "07_CSV_Integration",
        "08_JSON_Integration",
        "09_XML_Integration",
        "10_Parquet",
        "11_Data_Pipelines",
        "12_Automation",
        "13_Schema_Validation",
        "14_Data_Quality_Checks",
        "15_Incremental_Loading",
        "16_Batch_Processing",
        "17_Retry_and_Recovery",
        "18_Deduplication",
        "19_Data_Lineage",
        "20_Pipeline_Testing",
    ],

    # =========================================================
    # 07. ASYNCHRONOUS PROGRAMMING
    # =========================================================
    "07_Asynchronous_Programming": [
        "01_asyncio",
        "02_async_await",
        "03_Event_Loop",
        "04_Coroutines",
        "05_Task_Groups",
        "06_Concurrency",
        "07_Parallelism",
        "08_Multiprocessing",
        "09_Threading",
        "10_Concurrent_Futures",
        "11_Async_Context_Managers",
        "12_Async_Generators",
        "13_Cancellation_and_Timeouts",
        "14_Task_Management",
        "15_Semaphores_and_Locks",
        "16_Async_HTTP_Clients",
        "17_Async_Database_Operations",
        "18_Concurrency_Limits",
        "19_CPU_Bound_vs_IO_Bound_Work",
        "20_Concurrency_Testing",
    ],

    # =========================================================
    # 08. TESTING AND QUALITY ENGINEERING
    # =========================================================
    "08_Testing_and_Quality_Engineering": [
        "01_Pytest",
        "02_Test_Discovery_and_Assertions",
        "03_Fixtures",
        "04_Parametrized_Tests",
        "05_Mocking_and_Patching",
        "06_Unit_Testing",
        "07_Integration_Testing",
        "08_API_Testing",
        "09_Database_Testing",
        "10_Contract_Testing",
        "11_End_to_End_Testing",
        "12_Test_Coverage",
        "13_Property_Based_Testing",
        "14_Test_Data_Management",
        "15_Failure_and_Edge_Case_Testing",
        "16_Load_and_Stress_Testing",
        "17_Security_Testing",
        "18_Regression_Testing",
    ],

    # =========================================================
    # 09. MICROservices
    # =========================================================
    "09_Microservices": [
        "01_Microservices",
        "02_Monolith_vs_Microservices",
        "03_API_Gateway",
        "04_Service_Discovery",
        "05_Load_Balancing",
        "06_Inter_Service_Communication",
        "07_Synchronous_vs_Asynchronous_Communication",
        "08_Event_Driven_Architecture",
        "09_Circuit_Breaker",
        "10_Service_Mesh",
        "11_Service_Timeouts_and_Retries",
        "12_Idempotent_Consumers",
        "13_Distributed_Tracing",
        "14_Service_Resilience",
        "15_When_Not_to_Use_Microservices",
    ],

    # =========================================================
    # 10. MESSAGE QUEUES AND BACKGROUND TASKS
    # =========================================================
    "10_Message_Queues_and_Background_Tasks": [
        "01_Celery",
        "02_Redis",
        "03_RabbitMQ",
        "04_Kafka",
        "05_Background_Workers",
        "06_Scheduled_Jobs",
        "07_Task_Queues",
        "08_Retries_and_Dead_Letter_Queues",
        "09_Message_Delivery_Semantics",
        "10_At_Least_Once_and_At_Most_Once",
        "11_Deduplication_and_Idempotency",
        "12_Outbox_Pattern",
        "13_Task_Monitoring",
        "14_Worker_Scaling",
    ],

    # =========================================================
    # 11. AUTHENTICATION AND SECURITY
    # =========================================================
    "11_Authentication_and_Security": [
        "01_Authentication_vs_Authorization",
        "02_JWT",
        "03_OAuth2",
        "04_API_Keys",
        "05_Password_Hashing",
        "06_Password_Security",
        "07_Encryption_and_Key_Management",
        "08_HTTPS_and_TLS",
        "09_CORS",
        "10_CSRF",
        "11_RBAC",
        "12_Principle_of_Least_Privilege",
        "13_Input_Validation",
        "14_SQL_Injection_Prevention",
        "15_XSS_and_Injection_Risks",
        "16_SSRF_and_Request_Validation",
        "17_Secure_File_Uploads",
        "18_Rate_Limiting_and_Abuse_Prevention",
        "19_Secrets_Management",
        "20_Dependency_Vulnerability_Scanning",
        "21_Security_Headers",
        "22_Audit_Logging",
        "23_OWASP_API_Security",
        "24_Threat_Modeling",
    ],

    # =========================================================
    # 12. CLOUD AND DEPLOYMENT
    # =========================================================
    "12_Cloud_and_Deployment": [
        "01_Linux_Fundamentals",
        "02_Shell_and_Bash_Basics",
        "03_Processes_and_Signals",
        "04_Permissions_and_File_Systems",
        "05_Networking_Fundamentals",
        "06_DNS_and_TLS",
        "07_Reverse_Proxies",
        "08_AWS",
        "09_Google_Cloud",
        "10_Azure",
        "11_Object_Storage",
        "12_Secrets",
        "13_Environment_Variables",
        "14_Serverless",
        "15_Cloud_Architecture",
        "16_Domain_and_DNS_Configuration",
        "17_Deployment_Strategies",
        "18_Rollbacks",
        "19_Graceful_Shutdown",
        "20_Backup_and_Disaster_Recovery",
    ],

    # =========================================================
    # 13. CONTAINERIZATION
    # =========================================================
    "13_Containerization": [
        "01_Docker",
        "02_Dockerfile",
        "03_Docker_Compose",
        "04_Multi_Stage_Builds",
        "05_Image_Size_Optimization",
        "06_Non_Root_Containers",
        "07_Container_Networking",
        "08_Container_Volumes",
        "09_Container_Health_Checks",
        "10_Container_Registry",
        "11_Kubernetes",
        "12_Deployments_and_Services",
        "13_ConfigMaps_and_Secrets",
        "14_Resource_Limits",
        "15_Helm",
    ],

    # =========================================================
    # 14. PRODUCTION DEVOPS AND CI/CD
    # =========================================================
    "14_Production_DevOps": [
        "01_Git_and_GitHub_Workflow",
        "02_Branching_and_Code_Review",
        "03_GitHub_Actions",
        "04_CI_CD",
        "05_Automated_Testing_Pipeline",
        "06_Linting_and_Type_Checking",
        "07_Security_Scanning",
        "08_Dependency_Locking",
        "09_Build_and_Artifact_Management",
        "10_Automated_Deployment",
        "11_Environment_Promotion",
        "12_Versioning",
        "13_Release_Management",
        "14_Rollback_Strategy",
        "15_Database_Migrations_in_CI_CD",
        "16_Pre_Commit_Hooks",
        "17_Release_Checklists",
    ],

    # =========================================================
    # 15. MONITORING AND OBSERVABILITY
    # =========================================================
    "15_Monitoring_and_Observability": [
        "01_Prometheus",
        "02_Grafana",
        "03_OpenTelemetry",
        "04_Structured_Logging",
        "05_Distributed_Tracing",
        "06_Metrics",
        "07_Health_Checks",
        "08_Readiness_and_Liveness",
        "09_Performance_Monitoring",
        "10_Error_Tracking",
        "11_Request_Correlation_IDs",
        "12_Latency_and_Error_Rates",
        "13_Service_Level_Indicators",
        "14_Service_Level_Objectives",
        "15_Alerting",
        "16_Dashboards",
        "17_Incident_Investigation",
    ],

    # =========================================================
    # 16. SOFTWARE ARCHITECTURE AND SYSTEM DESIGN
    # =========================================================
    "16_Software_Architecture_and_System_Design": [
        "01_SOLID",
        "02_Design_Patterns",
        "03_Event_Driven_Architecture",
        "04_CQRS",
        "05_Saga_Pattern",
        "06_Message_Brokers",
        "07_Scalability",
        "08_Resilience",
        "09_Fault_Tolerance",
        "10_System_Design",
        "11_Load_Balancing",
        "12_Caching_Strategies",
        "13_Database_Scaling",
        "14_Replication_and_Partitioning",
        "15_Capacity_Estimation",
        "16_Consistency_and_Availability",
        "17_Distributed_System_Fundamentals",
        "18_Rate_Limiting_Algorithms",
        "19_Backpressure",
        "20_Failure_Mode_Analysis",
        "21_Cost_and_Tradeoff_Analysis",
    ],

    # =========================================================
    # 17. PERFORMANCE AND RELIABILITY ENGINEERING
    # =========================================================
    "17_Performance_and_Reliability_Engineering": [
        "01_Benchmarking",
        "02_CPU_and_Memory_Profiling",
        "03_Endpoint_Performance",
        "04_Database_Performance",
        "05_Query_Profiling",
        "06_Caching_and_Invalidation",
        "07_Load_Testing",
        "08_Stress_Testing",
        "09_Soak_Testing",
        "10_Connection_and_Resource_Limits",
        "11_Timeouts_and_Retries",
        "12_Circuit_Breakers",
        "13_Idempotency",
        "14_Graceful_Degradation",
        "15_Reliability_Budgets",
        "16_Incident_Response",
        "17_Postmortems",
    ],

    # =========================================================
    # 18. SCIENTIFIC COMPUTING - ADVANCED
    # =========================================================
    "18_Scientific_Computing_Advanced": [
        "01_NumPy_Advanced",
        "02_SciPy_Advanced",
        "03_Numba",
        "04_Cython",
        "05_JAX",
        "06_Dask",
        "07_xarray",
        "08_CuPy",
        "09_Sparse_Computing",
        "10_Optimization",
        "11_Simulation",
        "12_Numerical_Methods",
        "13_Vectorization",
        "14_Numerical_Stability",
        "15_Benchmarking_Scientific_Code",
    ],

    # =========================================================
    # 19. HIGH-PERFORMANCE COMPUTING
    # =========================================================
    "19_High_Performance_Computing": [
        "01_MPI4Py",
        "02_Parallel_Computing",
        "03_GPU_Computing",
        "04_CUDA_Python",
        "05_Distributed_Arrays",
        "06_Cluster_Computing",
        "07_Memory_and_Compute_Tradeoffs",
        "08_HPC_Workflow_Management",
    ],

    # =========================================================
    # 20. COMPUTATIONAL BIOLOGY
    # =========================================================
    "20_Computational_Biology": [
        "01_Biopython",
        "02_SeqIO",
        "03_Entrez",
        "04_BLAST",
        "05_PDB",
        "06_GenBank",
        "07_FASTA",
        "08_Multiple_Sequence_Alignment",
        "09_Phylogenetics",
        "10_Genome_Analysis",
        "11_Transcriptomics",
        "12_Proteomics",
        "13_Metabolomics",
        "14_Single_Cell_Analysis",
        "15_Spatial_Biology",
        "16_Biological_Data_Validation",
        "17_Reproducible_Computational_Research",
    ],

    # =========================================================
    # 21. BIOINFORMATICS TOOLKIT
    # =========================================================
    "21_Bioinformatics_Toolkit": [
        "01_PyMOL",
        "02_MDAnalysis",
        "03_PyRosetta",
        "04_Scanpy",
        "05_AnnData",
        "06_NetworkX",
        "07_BioPandas",
        "08_Pysam",
        "09_VCF_Processing",
        "10_GFF_Parsing",
        "11_Sequence_File_Formats",
        "12_Large_Biological_Datasets",
    ],

    # =========================================================
    # 22. CHEMINFORMATICS AND DRUG DISCOVERY
    # =========================================================
    "22_Cheminformatics_and_Drug_Discovery": [
        "01_RDKit",
        "02_OpenBabel",
        "03_DeepChem",
        "04_Molecular_Descriptors",
        "05_SMILES",
        "06_Molecular_Fingerprints",
        "07_Virtual_Screening",
        "08_Molecular_Docking",
        "09_QSAR",
        "10_Molecular_Dynamics",
        "11_OpenMM",
        "12_GROMACS_Integration",
        "13_Chemical_Data_Validation",
        "14_Drug_Discovery_Data_Pipelines",
    ],

    # =========================================================
    # 23. RESEARCH AUTOMATION
    # =========================================================
    "23_Research_Automation": [
        "01_PubMed_API",
        "02_CrossRef",
        "03_Semantic_Scholar",
        "04_OpenAlex",
        "05_arXiv",
        "06_Literature_Mining",
        "07_PDF_Extraction",
        "08_DOI_Processing",
        "09_Web_Scraping",
        "10_Automated_Reporting",
        "11_Metadata_Normalization",
        "12_Rate_Limits_and_Retry_Policies",
        "13_Research_Data_Provenance",
    ],

    # =========================================================
    # 24. DATA ENGINEERING
    # =========================================================
    "24_Data_Engineering": [
        "01_Apache_Arrow",
        "02_Parquet",
        "03_Polars",
        "04_DuckDB",
        "05_Data_Lakes",
        "06_Data_Warehouses",
        "07_Batch_Processing",
        "08_Stream_Processing",
        "09_Data_Schemas",
        "10_Data_Quality",
        "11_Incremental_Pipelines",
        "12_Pipeline_Orchestration",
        "13_Data_Partitioning",
        "14_Storage_Formats_and_Tradeoffs",
    ],

    # =========================================================
    # 25. AI DATA PIPELINES
    # =========================================================
    "25_AI_Data_Pipelines": [
        "01_ML_Data_Pipelines",
        "02_Feature_Stores",
        "03_Data_Versioning",
        "04_DVC",
        "05_MLflow",
        "06_WandB",
        "07_Model_Registry",
        "08_Data_Validation",
        "09_Model_Serving_APIs",
        "10_Model_Inference_Monitoring",
        "11_Reproducible_ML_Workflows",
    ],

    # =========================================================
    # 26. DISTRIBUTED COMPUTING
    # =========================================================
    "26_Distributed_Computing": [
        "01_Ray",
        "02_Dask_Distributed",
        "03_Spark_Basics",
        "04_Workflows",
        "05_Distributed_APIs",
        "06_Remote_Computing",
        "07_Distributed_Task_Execution",
        "08_Fault_Recovery",
        "09_Resource_Scheduling",
    ],

    # =========================================================
    # 27. CAPSTONE PROJECTS
    # =========================================================
    "27_Capstone_Projects": [
        "01_Genomics_API",
        "02_Protein_Analysis_Server",
        "03_Molecular_Docking_Pipeline",
        "04_Drug_Discovery_Backend",
        "05_Bioinformatics_Platform",
        "06_Multiomics_Data_Pipeline",
        "07_Literature_Mining_System",
        "08_ETL_System",
        "09_FastAPI_Microservice",
        "10_AI_Data_Infrastructure",
        "11_Digital_Twin_Biology_Platform",
        "12_Research_Knowledge_Graph",
        "13_Pharma_Data_Platform",
        "14_Scientific_Workflow_Manager",
        "15_End_to_End_Computational_Biology_Project",
        "16_Production_Ready_Backend_API",
        "17_API_with_PostgreSQL_and_Migrations",
        "18_Dockerized_Service_with_CI_CD",
        "19_Monitored_and_Load_Tested_API",
    ],
}


def ensure_directory(path: Path) -> None:
    """Create a directory and all missing parent directories."""
    path.mkdir(parents=True, exist_ok=True)


def create_placeholder_file(path: Path) -> None:
    """Create an empty file only if it does not already exist."""
    path.touch(exist_ok=True)


def build_roadmap(
    root: Path,
    structure: dict[str, Any],
) -> None:
    """Build the roadmap tree without overwriting existing files."""
    ensure_directory(root)

    for section_name, items in structure.items():
        section_dir = root / section_name
        ensure_directory(section_dir)

        for item in items:
            if isinstance(item, dict):
                for folder_name, children in item.items():
                    nested_dir = section_dir / folder_name
                    ensure_directory(nested_dir)
                    build_roadmap(nested_dir, children)
            else:
                topic_dir = section_dir / item
                ensure_directory(topic_dir)
                create_placeholder_file(topic_dir / "__init__.py")


def main() -> None:
    """Build the complete Advanced Python roadmap."""
    build_roadmap(ROOT_FOLDER, ROADMAP)
    print(f"Roadmap created or updated at: {ROOT_FOLDER.resolve()}")
    print("Existing files were preserved.")


if __name__ == "__main__":
    main()
