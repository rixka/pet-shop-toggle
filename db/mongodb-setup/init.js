use development;
db.createCollection('adoptions')
db.pets.createIndex({ name: 'text', animal: 'text' });
