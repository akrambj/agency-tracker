from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Agency tracker is running"}

# Clients 
class SocialMedia(BaseModel):
    platform: str
    link: str

class CreateClient(BaseModel):
    first_name: str
    last_name: str
    client_type: Literal["person", "company"]
    company_name: str | None = None
    social_media: list[SocialMedia] | None = None

class UpdateClient(BaseModel):
    first_name: str
    last_name: str
    client_type: Literal["person", "company"]
    company_name: str | None = None
    social_media: list[SocialMedia] | None = None


class Client(CreateClient):
    id: int


clients: list[Client] = [
    Client(
        id=1,
        first_name="Akram",
        last_name="Bedjaoui",
        client_type="person",
        social_media=[
            SocialMedia(platform="LinkedIn", link="https://linkedin.com/in/akram"),
            SocialMedia(platform="GitHub", link="https://github.com/akram"),
        ],
    ),
    Client(
        id=2,
        first_name="Sara",
        last_name="Benali",
        client_type="person",
        social_media=[
            SocialMedia(platform="Instagram", link="https://instagram.com/sara"),
        ],
    ),
    Client(
        id=3,
        first_name="Omar",
        last_name="Haddad",
        client_type="person",
        social_media=None,
    ),
    Client(
        id=4,
        first_name="Tech",
        last_name="Solutions",
        client_type="company",
        company_name="Tech Solutions LLC",
        social_media=[
            SocialMedia(platform="Twitter", link="https://twitter.com/techsolutions"),
            SocialMedia(platform="LinkedIn", link="https://linkedin.com/company/techsolutions"),
        ],
    ),
    Client(
        id=5,
        first_name="Digital",
        last_name="Agency",
        client_type="company",
        company_name="Digital Agency Pro",
        social_media=None,
    ),
    Client(
        id=6,
        first_name="Global",
        last_name="Industries",
        client_type="company",
        company_name="Global Industries Ltd",
        social_media=[
            SocialMedia(platform="Facebook", link="https://facebook.com/globalindustries"),
        ],
    ),
]

@app.get("/clients")
def get_clients():
    return {"message": "Client List returned", "data": clients}


@app.get("/clients/{id}")
def get_client(id: int):
    client = next((c for c in clients if c.id == id), None)
    if client is None:
        return {"message": "Client Not Found"}
    return {"message": "Client found", "data": client}


@app.post("/clients")
def create_client(client: CreateClient):
    new_id = max([c.id for c in clients], default=0) + 1
    new_client = Client(id=new_id, **client.model_dump())
    clients.append(new_client)
    return {"message": "Client has been created", "data": new_client}


@app.patch("/clients/{id}")
def update_client(id: int, updated_client: UpdateClient):
    # Find the existing client object
    existing_client = next((c for c in clients if c.id == id), None)
    if existing_client is None:
        return {"message": "Not found"}
    
    # Only update fields that were sent
    update_data = updated_client.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_client, key, value)
    
    return {"message": "Client updated", "data": existing_client}


@app.delete("/clients/{id}")
def remove_client(id: int):
    existing_client = next((c for c in clients if c.id == id), None)
    if existing_client is None:
        return {"message": "Not found"}
    clients.remove(existing_client)
    return {"message": "Client removed"}
