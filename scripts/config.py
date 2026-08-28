# scripts/config.py
"""
Configuration for GitHub Profile README Automation.
Allows manual control over featured repositories, exclusions, limits, and styling.
"""

GH_USERNAME = "madhanalagarsamy"

# Curated featured repositories to highlight in the profile
# Can be customized anytime without breaking automated updates
FEATURED_REPOSITORIES = [
    {
        "repo": "decimal-optical-transfer",
        "name": "Decimal Optical Transfer",
        "category": "Air-Gapped Systems / Fountain Coding",
        "tech": "TypeScript, LT Coding, Video Streams",
        "description": "Zero-network, screen-to-camera optical data transmission protocol supporting up to 1GB transfers via Fountain Codes (Luby Transform) and Duo-QR mosaic.",
        "url": "https://github.com/madhanalagarsamy/decimal-optical-transfer"
    },
    {
        "repo": "national-people-database-face-recognition-system",
        "name": "National People Database & Face Recognition",
        "category": "Computer Vision / Biometrics",
        "tech": "Python, OpenCV, SQLite3, Tkinter",
        "description": "Biometric citizen record management system featuring real-time camera capture, bounding box detection, and dual-engine facial verification.",
        "url": "https://github.com/madhanalagarsamy/national-people-database-face-recognition-system"
    },
    {
        "repo": "creative-corner-ecommerce",
        "name": "Creative Corner E-Commerce",
        "category": "Production Web & Security",
        "tech": "FastAPI, SQLAlchemy 2.0, Python 3.12+, Alembic",
        "description": "Production-grade e-commerce backend and SSR platform featuring a 4-tier magic-byte customer file validation pipeline, dynamic lead-time engine, and custom quote builder.",
        "url": "https://github.com/madhanalagarsamy/creative-corner-ecommerce"
    }
]

# Repositories to exclude from dynamic recent work list
EXCLUDED_REPOSITORIES = [
    "madhanalagarsamy",  # Profile repository
]

# Maximum number of recently updated repositories to show in dynamic recent section
MAX_RECENT_PROJECTS = 4

# Paths
README_PATH = "README.md"
BADGES_DIR = ".github/badges"
