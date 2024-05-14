from django.db import models
from django.contrib.auth.models import User

CATEGORY = ['Ai', 'Tech', 'Python', 'Java', 'C++', 'C#', 'Ruby', 'JavaScript', 'React', 'Angular', 'Vue', 'Django',
            'Flask', 'Express', 'Spring', 'Laravel', 'Node', 'RubyOnRails', 'ASP.NET', 'JQuery', 'Bootstrap',
            'Tailwind', 'Materialize', 'SemanticUI', 'Foundation', 'Bulma', 'UIKit', 'AntDesign', 'ChakraUI', 'Gatsby',
            'Next', 'Nuxt', 'Gridsome', 'Svelte', 'VuePress', 'ReactStatic', 'Docusaurus', 'Hugo', 'Jekyll', 'Hexo',
            'Ai', 'MachineLearning', 'DeepLearning', 'DataScience', 'BigData', 'DataAnalysis', 'DataEngineering',
            'DataMining', 'DataVisualization', 'BusinessIntelligence', 'ArtificialIntelligence', 'NaturalLanguageProcessing',
            'NaturalLanguageUnderstanding', 'SpeechRecognition', 'SpeechSynthesis', 'ReinforcementLearning',
            'Robotics', 'ComputerVision', 'CryptoCurrency', 'Blockchain', 'Bitcoin', 'Ethereum', 'Ripple', 'Litecoin']

class News(models.Model):
    title = models.CharField(max_length=200)
    short_description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    link = models.URLField(max_length=200)
    category = models.CharField(max_length=50, choices=[(x, x) for x in CATEGORY])

    def __str__(self):
        return self.title

class Rating(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return f'{self.user.username} rating'

class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} comment'

class Like(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('news', 'user')

    def __str__(self):
        return f'{self.user.username} likes {self.news.title}'
