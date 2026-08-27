"""Create an advanced Python learning roadmap directory structure.

This script is idempotent, production-oriented, and easy to extend.
It creates the full folder hierarchy and placeholder Python files using pathlib.Path.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


ROOT_FOLDER = Path("Advanced Python")


ROADMAP: dict[str, Any] = {
    "01_Professional_Python": [
        "01_Type_Hints",
        "02_Mypy",
        "03_Ruff",
        "04_Black",
        "05_isort",
        "06_Pre_commit",
        "07_Logging",
        "08_Config_Management",
        "09_Context_Managers",
        "10_Descriptors",
        "11_Metaclasses",
        "12_Advanced_Generators",
        "13_Memory_Management",
        "14_Garbage_Collection",
        "15_Profiling",
        "16_Debugging",
        "17_Packaging",
        "18_Publishing",
        "19_Python_Internals",
        "20_CPython_Overview",
    ],
    "02_Advanced_Backend_Development": [
        "01_Backend_Architecture",
        "02_Clean_Architecture",
        "03_Hexagonal_Architecture",
        "04_Layered_Architecture",
        "05_Domain_Driven_Design",
        "06_Service_Layer",
        "07_Repository_Pattern",
        "08_Dependency_Injection",
        "09_API_Architecture",
        "10_Project_Structure",
    ],
    "03_REST_API_Development": [
        "01_HTTP",
        "02_REST_Principles",
        "03_API_Design",
        "04_OpenAPI",
        "05_Swagger",
        "06_JSON",
        "07_XML",
        "08_API_Versioning",
        "09_Rate_Limiting",
        "10_Pagination",
        "11_Filtering",
        "12_API_Testing",
        "13_Postman",
        "14_HTTPX",
        "15_Requests",
    ],
    "04_FastAPI_Professional": [
        "01_FastAPI_Basics",
        "02_Routers",
        "03_Dependency_INJECTION",
        "04_Pydantic",
        "05_Request_Validation",
        "06_Response_Models",
        "07_File_Uploads",
        "08_Background_Tasks",
        "09_WebSockets",
        "10_Middleware",
        "11_CORS",
        "12_JWT",
        "13_OAuth2",
        "14_FastAPI_Security",
        "15_Production_Deployment",
    ],
    "05_Database_Engineering": [
        "01_SQL",
        "02_PostgreSQL",
        "03_SQLAlchemy",
        "04_SQLModel",
        "05_Alembic",
        "06_ORM",
        "07_CRUD",
        "08_Indexes",
        "09_Transactions",
        "10_Connection_Pooling",
        "11_Query_Optimization",
        "12_Database_Design",
        "13_Normalization",
        "14_Views",
        "15_Stored_Procedures",
    ],
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
    ],
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
    ],
    "08_Microservices": [
        "01_Microservices",
        "02_API_Gateway",
        "03_Service_Discovery",
        "04_Load_Balancing",
        "05_Inter_Service_Communication",
        "06_Event_Driven_Architecture",
        "07_Circuit_Breaker",
        "08_Service_Mesh",
    ],
    "09_Message_Queues_and_Background_Tasks": [
        "01_Celery",
        "02_Redis",
        "03_RabbitMQ",
        "04_Kafka",
        "05_Background_Workers",
        "06_Scheduled_Jobs",
        "07_Task_Queues",
    ],
    "10_Authentication_and_Security": [
        "01_JWT",
        "02_OAuth2",
        "03_API_Keys",
        "04_Encryption",
        "05_Hashing",
        "06_Password_Security",
        "07_HTTPS",
        "08_CORS",
        "09_CSRF",
        "10_RBAC",
    ],
    "11_Cloud_and_Deployment": [
        "01_AWS",
        "02_Google_Cloud",
        "03_Azure",
        "04_Object_Storage",
        "05_Secrets",
        "06_Environment_Variables",
        "07_Serverless",
        "08_Cloud_Architecture",
    ],
    "12_Containerization": [
        "01_Docker",
        "02_Dockerfile",
        "03_Docker_Compose",
        "04_Kubernetes",
        "05_Helm",
        "06_Container_Registry",
    ],
    "13_Production_DevOps": [
        "01_GitHub_Actions",
        "02_CI_CD",
        "03_Testing_Pipeline",
        "04_Linting",
        "05_Automated_Deployment",
        "06_Versioning",
        "07_Release_Management",
    ],
    "14_Scientific_Computing_Advanced": [
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
    ],
    "15_High_Performance_Computing": [
        "01_MPI4Py",
        "02_Parallel_Computing",
        "03_GPU_Computing",
        "04_CUDA_Python",
        "05_Distributed_Arrays",
        "06_Cluster_Computing",
    ],
    "16_Computational_Biology": [
        "01_Biopython",
        "02_SeqIO",
        "03_Entrez",
        "04_BLAST",
        "05_PDB",
        "06_GenBank",
        "07_FASTA",
        "08_MSA",
        "09_Phylogenetics",
        "10_Genome_Analysis",
        "11_Transcriptomics",
        "12_Proteomics",
        "13_Metabolomics",
        "14_Single_Cell_Analysis",
        "15_Spatial_Biology",
    ],
    "17_Bioinformatics_Toolkit": [
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
    ],
    "18_Cheminformatics_and_Drug_Discovery": [
        "01_RDKit",
        "02_OpenBabel",
        "03_DeepChem",
        "04_Molecular_Descriptors",
        "05_SMILES",
        "06_Molecular_Fingerprints",
        "07_Virtual_Screening",
        "08_Docking",
        "09_QSAR",
        "10_Molecular_Dynamics",
        "11_OpenMM",
        "12_GROMACS_Integration",
    ],
    "19_Research_Automation": [
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
    ],
    "20_Data_Engineering": [
        "01_Apache_Arrow",
        "02_Parquet",
        "03_Polars",
        "04_DuckDB",
        "05_DataLake",
        "06_DataWarehouse",
        "07_Batch_Processing",
        "08_Stream_Processing",
    ],
    "21_AI_Data_Pipelines": [
        "01_ML_Data_Pipeline",
        "02_Feature_Store",
        "03_Data_Versioning",
        "04_DVC",
        "05_MLflow",
        "06_WandB",
        "07_Model_Registry",
        "08_Data_Validation",
    ],
    "22_Distributed_Computing": [
        "01_Ray",
        "02_Dask_Distributed",
        "03_Spark_Basics",
        "04_Workflows",
        "05_Distributed_APIs",
        "06_Remote_Computing",
    ],
    "23_Monitoring_and_Observability": [
        "01_Prometheus",
        "02_Grafana",
        "03_OpenTelemetry",
        "04_Structured_Logging",
        "05_Tracing",
        "06_Metrics",
        "07_Health_Checks",
        "08_Performance_Monitoring",
    ],
    "24_Software_Architecture": [
        "01_SOLID",
        "02_Design_Patterns",
        "03_Event_Driven_Architecture",
        "04_CQRS",
        "05_Saga_Pattern",
        "06_Message_Broker",
        "07_Scalability",
        "08_Resilience",
        "09_Fault_Tolerance",
        "10_System_Design",
    ],
    "25_Capstone_Projects": [
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
    ],
}


def ensure_directory(path: Path) -> None:
    """Create a directory and its parents if they do not already exist."""
    path.mkdir(parents=True, exist_ok=True)


def create_placeholder_file(path: Path) -> None:
    """Create an empty Python file without overwriting an existing one."""
    path.touch(exist_ok=True)


def build_roadmap(root: Path, structure: dict[str, Any]) -> None:
    """Build the complete directory tree from a nested roadmap structure."""
    ensure_directory(root)

    for phase_name, items in structure.items():
        phase_dir = root / phase_name
        ensure_directory(phase_dir)

        for item in items:
            if isinstance(item, dict):
                for folder_name, children in item.items():
                    topic_dir = phase_dir / folder_name
                    ensure_directory(topic_dir)
                    build_roadmap(topic_dir, children)
            else:
                topic_dir = phase_dir / item
                ensure_directory(topic_dir)
                create_placeholder_file(topic_dir / "__init__.py")


def main() -> None:
    """Entry point for script execution."""
    build_roadmap(ROOT_FOLDER, ROADMAP)


if __name__ == "__main__":
    main()