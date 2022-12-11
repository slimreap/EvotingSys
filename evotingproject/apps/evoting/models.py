
from django.db import models
from evotingproject.apps.accounts.models import UserProfile



class Platform(models.Model):
    candidate_platform = models.CharField(max_length=50)
    candidate_platform2 = models.CharField(max_length=50)
    candidate_platform3 = models.CharField(max_length=50)
    def __str__(self):
        return self.candidate_platform

class Position(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    

class PartyList(models.Model):
    partylist_name = models.CharField(max_length=100)
    
   
    def __str__(self):
        return self.partylist_name

class CandidateProfile(models.Model):
    Candidate_Img = models.ImageField(upload_to='images/',null=True)
    name = models.CharField(max_length=200) 
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name='platform',null=True)
    partylist = models.ForeignKey(PartyList, on_delete=models.CASCADE, related_name='partylist',null=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='position',null=True)


    def __str__(self):
        return self.name

class votes(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='candidate')
    voter = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='voter')
    


    def __str__(self):
        return str(self.candidate)

class votetracker(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='candidatevotetracker')
    vote_count = models.IntegerField(default=0,null=True)