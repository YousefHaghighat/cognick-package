# cognick-package

Reusable Django package for working with Cognick cognitive parameters.

## Get Started

```bash
pip install cognick
```

### Main Settings Configuration
Add the following settings to your Django settings.py:

```python

# redis config
REDIS_HOST="<your_redis_host>"
REDIS_PORT="<your_redis_port>"
REDIS_SELECT_DB="<your_redis_db>"
COGNICK_COGNITIVE_CACHE_TIMEOUT="<redis_cache_timeout>" # optional (default=3600)

# cognitive parameters list url
COGNICK_COGNITIVE_URL="<your_cog_params_url>"

```
COGNICK_COGNITIVE_URL must point to the Cognick cognitive parameters list endpoint.

---

### Usage
Use Cognick cognitive parameters directly in your Django models.


#### Model

```python
from django.db import models
from cognick.cognitive.fields import CognitiveField, CognitiveArrayField


class Game(models.Model):
    ...
    primary_cognitive_parameter = CognitiveField()
    cognitive_parameters = CognitiveArrayField()
    ...

```
The values are stored as cognitive parameter IDs in the database,
while the package resolves them to CognitiveParameter objects when accessed.

#### Serializer
Use CognitiveParameterSerializer to return the complete cognitive parameter data dynamically.

```python
from rest_framework import serializers

from models import Game
from cognick.cognitive.serializers import CognitiveParameterSerializer

class GameSerializer(serializers.ModelSerializer):
    primary_cognitive_parameter = CognitiveParameterSerializer()
    cognitive_parameters = CognitiveParameterSerializer(many=True)
    
    class Meta:
        model = Game
        fields = '__all__'
        
```
The serializer is dynamic and returns the fields available in the Cognick API response.

You do not need to manually define fields such as name_fa, name_en, description_fa, etc.

### Accessing Cognitive Parameters

#### Single Cognitive Parameter
```python
game = Game.objects.get(id=1)

game.primary_cognitive_parameter.name_fa
game.primary_cognitive_parameter.name_en
game.primary_cognitive_parameter.description_fa
```

