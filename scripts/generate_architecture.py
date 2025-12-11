#!/usr/bin/env python3
"""Generate architecture diagram"""
import os
import sys

def generate_ascii_diagram():
    """Generate ASCII architecture diagram"""
    diagram = """
╔═══════════════════════════════════════════════════════════════╗
║                    TESTING PLATFORM ARCHITECTURE              ║
╚═══════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────┐
│                       CLIENT LAYER                           │
│  Web Browsers: Chrome, Firefox, Edge, Safari                 │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTPS/TLS
┌──────────────────────▼──────────────────────────────────────┐
│                  PRESENTATION LAYER                          │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Templates  │  │  Static CSS  │  │ JavaScript   │       │
│  │  (Jinja2)   │  │  Bootstrap5  │  │ Timer/AJAX   │       │
│  └─────────────┘  └──────────────┘  └──────────────┘       │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                  APPLICATION LAYER                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │  Auth    │ │  Admin   │ │ Teacher  │ │ Student  │      │
│  │Blueprint │ │Blueprint │ │Blueprint │ │Blueprint │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   BUSINESS LAYER                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │AuthSvc   │ │TestSvc   │ │Question  │ │Result    │      │
│  │UserSvc   │ │TermsSvc  │ │Svc       │ │Svc       │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
│  ┌───────────────────────┐ ┌──────────────────────┐        │
│  │  EncryptionService    │ │  FileParserService   │        │
│  │  (AES-256-GCM)        │ │  (Word/PowerPoint)   │        │
│  └───────────────────────┘ └──────────────────────┘        │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                      DATA LAYER                              │
│  SQLAlchemy ORM                                              │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐             │
│  │ User │ │ Test │ │Quest.│ │Result│ │Assign│             │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘             │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                PERSISTENCE LAYER                             │
│  MySQL/PostgreSQL Database + Encrypted File Storage          │
└─────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════
                    SECURITY LAYERS
═══════════════════════════════════════════════════════════════
Transport:      HTTPS/TLS
Authentication: Flask-Login + Bcrypt
Authorization:  RBAC (admin/teacher/student)
Application:    CSRF + Rate Limiting
Data:           AES-256-GCM Encryption
Audit:          Comprehensive Logging
═══════════════════════════════════════════════════════════════
"""
    return diagram


def save_diagram(output_path='architecture.txt'):
    """Save diagram to file"""
    diagram = generate_ascii_diagram()
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(diagram)
    
    print(f"✓ Architecture diagram saved to: {output_path}")
    print(f"  Size: {len(diagram)} characters")


def main():
    """Main function"""
    print("="*60)
    print("Architecture Diagram Generator")
    print("="*60)
    
    # Get output path
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'docs')
    output_file = os.path.join(output_dir, 'architecture_diagram.txt')
    
    # Generate and save
    save_diagram(output_file)
    
    # Also print to console
    print("\n" + generate_ascii_diagram())
    
    print("\n" + "="*60)
    print("Diagram generation completed!")
    print("="*60)


if __name__ == '__main__':
    main()
