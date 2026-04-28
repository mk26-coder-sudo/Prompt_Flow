# 🚀 PromptFlow  
### Build • Version • Collaborate • Improve

A **DBMS-driven full-stack application** for managing prompts with version control, collaboration, and activity tracking.

---

## 🌟 Why PromptFlow?

In real-world systems, content evolves through iterations and collaboration.

PromptFlow solves this by providing:
- Structured **version control**
- Controlled **collaboration**
- Transparent **activity tracking**

All powered by a well-designed relational database.

---

## 🎯 Key Highlights

- 🧠 **Version Control System** for prompts  
- 🤝 **Role-based Sharing (View/Edit)**  
- ⭐ **Best Version Identification (Auto-managed)**  
- 📊 **Activity Logging (Audit Trail)**  
- 🗂️ **Project-wise Organization**  
- 🧱 **Normalized Relational Database Design**

---

## 🧠 Core Features

### 🗂️ Project Management
- Create and organize projects
- Group prompts efficiently

---

### 🧾 Prompt Versioning
- Multiple versions per prompt
- Tracks:
  - Version number
  - Content
  - Contributor
- Sorted using:
```sql
ORDER BY is_best DESC, version_number DESC

### ⭐ Best Version System
Latest version is automatically treated as best
Ensures:
No conflicts
Clean UX
Single source of truth

### 🤝 Collaboration System
Share prompts via email
Permissions:
View
Edit
Enables multi-user contribution

### 📊 Activity Tracking

Logs all important actions:

CREATE_PROMPT
ADD_VERSION
SHARE_PROMPT

Includes:

Username
Action
Timestamp

### 🗄️ Database Design (DBMS Focus)
🔹 Entities
Users
Projects
Prompts
Versions
Shares
Activity

### 🔹 Relationships
One-to-Many → Users → Projects
One-to-Many → Projects → Prompts
One-to-Many → Prompts → Versions
Many-to-Many → Users ↔ Prompts (via Shares)

### 🔹 Normalization
Database designed up to 3NF
Eliminates redundancy
Maintains consistency

### 🔹 Constraints
PRIMARY KEY
FOREIGN KEY
NOT NULL
ENUM (permissions)

### ⚙️ Tech Stack
Backend
Python (Flask)
Database
MySQL
Frontend
HTML
Tailwind CSS
JavaScript

### 🔄 System Workflow
User logs in
Creates project
Adds prompt
Creates versions
Latest version becomes best
Shares prompt
Collaborators contribute
Activity gets logged

### -- Get versions (best first)
SELECT * FROM Versions
WHERE prompt_id = ?
ORDER BY is_best DESC, version_number DESC;

-- Get shared projects
SELECT DISTINCT p.project_id, p.title
FROM Shares s
JOIN Prompts pr ON s.prompt_id = pr.prompt_id
JOIN Projects p ON pr.project_id = p.project_id;

git clone https://github.com/YOUR_USERNAME/PromptFlow.git
cd PromptFlow

pip install -r requirements.txt
python app.py

##Open:

http://127.0.0.1:5000

### 📸 Demo

### 🧠 What I Learned
Designing normalized relational schemas
Handling real-world relationships (1:M, M:M)
Implementing version control logic
Managing data integrity in DBMS
Building full-stack systems around database design

### design
🚀 Future Improvements
Indexing for performance
Stored procedures & triggers
Real-time collaboration
Search & filtering
AI-based prompt suggestions
