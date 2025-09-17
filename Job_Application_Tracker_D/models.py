class JobApplication:
    def __init__(self, id=None, company="", role="", status="Applied", deadline=None, notes=""):
        self.id = id
        self.company = company
        self.role = role
        self.status = status
        self.deadline = deadline
        self.notes = notes
    
    def to_dict(self):
        return {
            "id": self.id,
            "company": self.company,
            "role": self.role,
            "status": self.status,
            "deadline": self.deadline,
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            company=data.get("company", ""),
            role=data.get("role", ""),
            status=data.get("status", "Applied"),
            deadline=data.get("deadline"),
            notes=data.get("notes", "")
        )