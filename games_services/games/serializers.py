from rest_framework import serializers, generics
from rest_framework.reverse import reverse

from games.models import EsrbRating
from games.models import Game
from games.models import Player
from games.models import PlayerScore
import games.views


class EsrbRatingSerializer(serializers.HyperlinkedModelSerializer):
    games = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='game-detail')

    class Meta:
        model = EsrbRating
        fields = ('url', 'id', 'description', 'games')


class GameSerializer(serializers.HyperlinkedModelSerializer):
    # We want to display the game ESRB rating description instead of its id
    esrb_rating = serializers.SlugRelatedField(
        queryset=EsrbRating.objects.all(),
        slug_field='description')

    class Meta:
        model = Game
        fields = (
            'url',
            'esrb_rating',
            'name',
            'release_date',
            'played_once',
            'played_times')


class ScoreSerializer(serializers.HyperlinkedModelSerializer):
    # We want to display all the details for the related game
    game = GameSerializer()

    # We don't include the player because a score will be nested in the player

    class Meta:
        model = PlayerScore
        fields = (
            'url',
            'id',
            'score',
            'score_date',
            'game')


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    scores = ScoreSerializer(many=True, read_only=True)
    gender = serializers.ChoiceField(
        choices=Player.GENDER_CHOICES)
    gender_description = serializers.CharField(
        source='get_gender_display',
        read_only=True)

    class Meta:
        model = Player
        fields = (
            'url',
            'name',
            'gender',
            'gender_description',
            'scores')


class PlayerScoreSerializer(serializers.ModelSerializer):
    # We want to display the players's name instead of its id
    player = serializers.SlugRelatedField(queryset=Player.objects.all(), slug_field='name')
    # We want to display the game's name instead of its id
    game = serializers.SlugRelatedField(queryset=Game.objects.all(), slug_field='name')

    class Meta:
        model = PlayerScore
        fields = (
            'url',
            'id',
            'score',
            'score_date',
            'player',
            'game')
