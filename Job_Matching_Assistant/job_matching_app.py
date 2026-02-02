import pandas as pd
import random
from collections import deque

class JobSearch:
    def __init__(self, jobs_file='jobs.csv'):
        self.jobs_file = jobs_file
        self.jobs = self.load_jobs()
    
    def load_jobs(self):
        """Load jobs from CSV file"""
        try:
            return pd.read_csv(self.jobs_file)
        except FileNotFoundError:
            return pd.DataFrame(columns=[
                'Job Title', 'Required Skills', 'Location', 'Salary', 'Company'
            ])
    
    def save_jobs(self):
        """Save jobs to CSV file"""
        self.jobs.to_csv(self.jobs_file, index=False)
    
    def get_all_jobs(self):
        """Get all jobs"""
        return self.jobs
    
    def build_job_graph(self):
        """Build graph representation of jobs"""
        graph = {}
        
        for idx, job in self.jobs.iterrows():
            node_id = f"job_{idx}"
            graph[node_id] = {
                'data': job.to_dict(),
                'neighbors': []
            }
            
            # Connect jobs with similar required skills
            for idx2, job2 in self.jobs.iterrows():
                if idx != idx2:
                    node_id2 = f"job_{idx2}"
                    # Check if jobs share at least one required skill
                    skills1 = set(str(job['Required Skills']).lower().split(', '))
                    skills2 = set(str(job2['Required Skills']).lower().split(', '))
                    if skills1.intersection(skills2):
                        graph[node_id]['neighbors'].append(node_id2)
        
        return graph
    
    def search_jobs_bfs(self, user_skills, user_location):
        """Search jobs using BFS algorithm"""
        graph = self.build_job_graph()
        user_skills_set = set([skill.lower() for skill in user_skills])
        user_location = user_location.lower()
        
        matching_jobs = []
        visited = set()
        queue = deque()
        
        # Start BFS from all job nodes
        for node_id in graph.keys():
            if node_id not in visited:
                queue.append(node_id)
                visited.add(node_id)
                
                while queue:
                    current_node = queue.popleft()
                    job_data = graph[current_node]['data']
                    
                    # Check if job matches user skills and location
                    job_skills = set(str(job_data['Required Skills']).lower().split(', '))
                    job_location = str(job_data['Location']).lower()
                    
                    skill_match = len(user_skills_set.intersection(job_skills)) > 0
                    location_match = user_location in job_location or 'remote' in job_location or 'any' in job_location
                    
                    if skill_match and location_match:
                        matching_jobs.append(job_data)
                    
                    # Add neighbors to queue
                    for neighbor in graph[current_node]['neighbors']:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
        
        # Sort by number of matching skills
        matching_jobs.sort(
            key=lambda x: len(user_skills_set.intersection(
                set(str(x['Required Skills']).lower().split(', '))
            )),
            reverse=True
        )
        
        return matching_jobs
    
    def search_jobs_dfs(self, user_skills, user_location, max_depth=3):
        """Search jobs using DFS algorithm"""
        graph = self.build_job_graph()
        user_skills_set = set([skill.lower() for skill in user_skills])
        user_location = user_location.lower()
        
        matching_jobs = []
        visited = set()
        
        def dfs(node_id, depth):
            if depth > max_depth or node_id in visited:
                return
            
            visited.add(node_id)
            job_data = graph[node_id]['data']
            
            # Check if job matches user skills and location
            job_skills = set(str(job_data['Required Skills']).lower().split(', '))
            job_location = str(job_data['Location']).lower()
            
            skill_match = len(user_skills_set.intersection(job_skills)) > 0
            location_match = user_location in job_location or 'remote' in job_location or 'any' in job_location
            
            if skill_match and location_match:
                matching_jobs.append(job_data)
            
            # Recursively visit neighbors
            for neighbor in graph[node_id]['neighbors']:
                dfs(neighbor, depth + 1)
        
        # Start DFS from all job nodes
        for node_id in graph.keys():
            if node_id not in visited:
                dfs(node_id, 0)
        
        # Sort by number of matching skills
        matching_jobs.sort(
            key=lambda x: len(user_skills_set.intersection(
                set(str(x['Required Skills']).lower().split(', '))
            )),
            reverse=True
        )
        
        return matching_jobs
    
    def generate_dummy_data(self):
        """Generate dummy job data"""
        job_titles = [
            "Software Engineer", "Data Scientist", "Web Developer",
            "DevOps Engineer", "UX Designer", "Product Manager",
            "Machine Learning Engineer", "Cloud Architect",
            "Cybersecurity Analyst", "Database Administrator",
            "Frontend Developer", "Backend Developer", "Full Stack Developer",
            "Mobile App Developer", "AI Researcher", "Network Engineer"
        ]
        
        skills = [
            "python", "java", "javascript", "react", "node.js",
            "sql", "aws", "docker", "kubernetes", "machine learning",
            "data analysis", "html", "css", "git", "rest api",
            "mongodb", "postgresql", "linux", "agile", "scrum"
        ]
        
        locations = [
            "New York", "San Francisco", "Austin", "Seattle",
            "Boston", "Chicago", "Los Angeles", "Remote",
            "London", "Berlin", "Toronto", "Singapore"
        ]
        
        companies = [
            "TechCorp", "DataSystems", "WebSolutions", "CloudTech",
            "InnovateInc", "FutureWorks", "DigitalDreams", "ByteMasters",
            "CodeCrafters", "AI Innovations", "CyberSecure", "NetWorks"
        ]
        
        jobs_data = []
        
        for i in range(50):  # Generate 50 dummy jobs
            title = random.choice(job_titles)
            num_skills = random.randint(2, 5)
            job_skills = random.sample(skills, num_skills)
            location = random.choice(locations)
            salary = f"${random.randint(60, 150)}k/year"
            company = random.choice(companies)
            
            jobs_data.append({
                'Job Title': title,
                'Required Skills': ', '.join(job_skills),
                'Location': location,
                'Salary': salary,
                'Company': company
            })
        
        self.jobs = pd.DataFrame(jobs_data)
        self.save_jobs()
        return self.jobs