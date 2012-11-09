# -*- coding: utf-8 -*-

import json, unittest
import requests
from django.test import TestCase


class InterfaceTest( TestCase ):
  
  def test_keywords_get(self):
    url = u'http://127.0.0.1/services/nlp/keywords/'
    params = {
      u'text': u'''
      Four score and seven years ago our fathers brought forth on this continent a new nation, conceived in liberty, and dedicated to the proposition that all men are created equal.
      Now we are engaged in a great civil war, testing whether that nation, or any nation, so conceived and so dedicated, can long endure. We are met on a great battle-field of that war. We have come to dedicate a portion of that field, as a final resting place for those who here gave their lives that that nation might live. It is altogether fitting and proper that we should do this.
      But, in a larger sense, we can not dedicate, we can not consecrate, we can not hallow this ground. The brave men, living and dead, who struggled here, have consecrated it, far above our poor power to add or detract. The world will little note, nor long remember what we say here, but it can never forget what they did here. It is for us the living, rather, to be dedicated here to the unfinished work which they who fought here have thus far so nobly advanced. It is rather for us to be here dedicated to the great task remaining before us—that from these honored dead we take increased devotion to that cause for which they gave the last full measure of devotion—that we here highly resolve that these dead shall not have died in vain—that this nation, under God, shall have a new birth of freedom—and that government of the people, by the people, for the people, shall not perish from the earth.
      '''
      }
    r = requests.get( url, params=params )
    self.assertEqual( 200, r.status_code )
    d = json.loads( r.text )
    self.assertEqual( [u'count_keywords_stemmed', u'count_keywords_unstemmed', u'count_keywords_unstemmed_additional', u'count_words_repeating_stemmed', u'count_words_repeating_unstemmed', u'count_words_total', u'keywords_stemmed', u'keywords_unstemmed', u'keywords_unstemmed_additional', u'repeating_words_unstemmed', u'time_start', u'time_taken'], sorted(d.keys()) )
  
  def test_keywords_post(self):
    url = u'http://127.0.0.1/services/nlp/keywords/'
    params = {
      u'text': u'''
      Thank you so much. 

      Tonight, more than 200 years after a former colony won the right to determine its own destiny, the task of perfecting our union moves forward. 

      It moves forward because of you. It moves forward because you reaffirmed the spirit that has triumphed over war and depression, the spirit that has lifted this country from the depths of despair to the great heights of hope, the belief that while each of us will pursue our own individual dreams, we are an American family and we rise or fall together as one nation and as one people.

      Tonight, in this election, you, the American people, reminded us that while our road has been hard, while our journey has been long, we have picked ourselves up, we have fought our way back, and we know in our hearts that for the United States of America the best is yet to come. 

      I want to thank every American who participated in this election, whether you voted for the very first time or waited in line for a very long time. By the way, we have to fix that. Whether you pounded the pavement or picked up the phone, whether you held an Obama sign or a Romney sign, you made your voice heard and you made a difference. 

      I just spoke with Gov. Romney and I congratulated him and Paul Ryan on a hard-fought campaign. We may have battled fiercely, but it's only because we love this country deeply and we care so strongly about its future. From George to Lenore to their son Mitt, the Romney family has chosen to give back to America through public service and that is the legacy that we honor and applaud tonight. In the weeks ahead, I also look forward to sitting down with Gov. Romney to talk about where we can work together to move this country forward. 

      I want to thank my friend and partner of the last four years, America's happy warrior, the best vice president anybody could ever hope for, Joe Biden. 

      And I wouldn't be the man I am today without the woman who agreed to marry me 20 years ago. Let me say this publicly: Michelle, I have never loved you more. I have never been prouder to watch the rest of America fall in love with you, too, as our nation's first lady. Sasha and Malia, before our very eyes you're growing up to become two strong, smart beautiful young women, just like your mom. And I'm so proud of you guys. But I will say that for now one dog's probably enough. 

      To the best campaign team and volunteers in the history of politics. The best. The best ever. Some of you were new this time around, and some of you have been at my side since the very beginning. But all of you are family. No matter what you do or where you go from here, you will carry the memory of the history we made together and you will have the lifelong appreciation of a grateful president. Thank you for believing all the way, through every hill, through every valley. You lifted me up the whole way and I will always be grateful for everything that you've done and all the incredible work that you put in. 

      I know that political campaigns can sometimes seem small, even silly. And that provides plenty of fodder for the cynics that tell us that politics is nothing more than a contest of egos or the domain of special interests. But if you ever get the chance to talk to folks who turned out at our rallies and crowded along a rope line in a high school gym, or saw folks working late in a campaign office in some tiny county far away from home, you'll discover something else. 

      You'll hear the determination in the voice of a young field organizer who's working his way through college and wants to make sure every child has that same opportunity. You'll hear the pride in the voice of a volunteer who's going door to door because her brother was finally hired when the local auto plant added another shift. You'll hear the deep patriotism in the voice of a military spouse who's working the phones late at night to make sure that no one who fights for this country ever has to fight for a job or a roof over their head when they come home. 

      That's why we do this. That's what politics can be. That's why elections matter. It's not small, it's big. It's important. Democracy in a nation of 300 million can be noisy and messy and complicated. We have our own opinions. Each of us has deeply held beliefs. And when we go through tough times, when we make big decisions as a country, it necessarily stirs passions, stirs up controversy. 

      That won't change after tonight, and it shouldn't. These arguments we have are a mark of our liberty. We can never forget that as we speak people in distant nations are risking their lives right now just for a chance to argue about the issues that matter, the chance to cast their ballots like we did today. 

      But despite all our differences, most of us share certain hopes for America's future. We want our kids to grow up in a country where they have access to the best schools and the best teachers. A country that lives up to its legacy as the global leader in technology and discovery and innovation, with all the good jobs and new businesses that follow. 

      We want our children to live in an America that isn't burdened by debt, that isn't weakened by inequality, that isn't threatened by the destructive power of a warming planet. We want to pass on a country that's safe and respected and admired around the world, a nation that is defended by the strongest military on earth and the best troops this -- this world has ever known. But also a country that moves with confidence beyond this time of war, to shape a peace that is built on the promise of freedom and dignity for every human being. 

      We believe in a generous America, in a compassionate America, in a tolerant America, open to the dreams of an immigrant's daughter who studies in our schools and pledges to our flag. To the young boy on the south side of Chicago who sees a life beyond the nearest street corner. To the furniture worker's child in North Carolina who wants to become a doctor or a scientist, an engineer or an entrepreneur, a diplomat or even a president -- that's the future we hope for. That's the vision we share. That's where we need to go -- forward. That's where we need to go. 

      Now, we will disagree, sometimes fiercely, about how to get there. As it has for more than two centuries, progress will come in fits and starts. It's not always a straight line. It's not always a smooth path. By itself, the recognition that we have common hopes and dreams won't end all the gridlock or solve all our problems or substitute for the painstaking work of building consensus and making the difficult compromises needed to move this country forward. But that common bond is where we must begin. 

      Our economy is recovering. A decade of war is ending. A long campaign is now over. And whether I earned your vote or not, I have listened to you, I have learned from you, and you've made me a better president. And with your stories and your struggles, I return to the White House more determined and more inspired than ever about the work there is to do and the future that lies ahead. 

      Tonight you voted for action, not politics as usual. You elected us to focus on your jobs, not ours. And in the coming weeks and months, I am looking forward to reaching out and working with leaders of both parties to meet the challenges we can only solve together. Reducing our deficit. Reforming our tax code. Fixing our immigration system. Freeing ourselves from foreign oil. We've got more work to do. 

      But that doesn't mean your work is done. The role of citizen in our democracy does not end with your vote. America's never been about what can be done for us. It's about what can be done by us together through the hard and frustrating, but necessary work of self-government. That's the principle we were founded on. 

      This country has more wealth than any nation, but that's not what makes us rich. We have the most powerful military in history, but that's not what makes us strong. Our university, our culture are all the envy of the world, but that's not what keeps the world coming to our shores. 

      What makes America exceptional are the bonds that hold together the most diverse nation on earth. The belief that our destiny is shared; that this country only works when we accept certain obligations to one another and to future generations. The freedom which so many Americans have fought for and died for come with responsibilities as well as rights. And among those are love and charity and duty and patriotism. That's what makes America great. 

      I am hopeful tonight because I've seen the spirit at work in America. I've seen it in the family business whose owners would rather cut their own pay than lay off their neighbors, and in the workers who would rather cut back their hours than see a friend lose a job. I've seen it in the soldiers who reenlist after losing a limb and in those SEALs who charged up the stairs into darkness and danger because they knew there was a buddy behind them watching their back. 

      I've seen it on the shores of New Jersey and New York, where leaders from every party and level of government have swept aside their differences to help a community rebuild from the wreckage of a terrible storm. And I saw just the other day, in Mentor, Ohio, where a father told the story of his 8-year-old daughter, whose long battle with leukemia nearly cost their family everything had it not been for health care reform passing just a few months before the insurance company was about to stop paying for her care. 

      I had an opportunity to not just talk to the father, but meet this incredible daughter of his. And when he spoke to the crowd listening to that father's story, every parent in that room had tears in their eyes, because we knew that little girl could be our own. And I know that every American wants her future to be just as bright. That's who we are. That's the country I'm so proud to lead as your president. 

      And tonight, despite all the hardship we've been through, despite all the frustrations of Washington, I've never been more hopeful about our future. I have never been more hopeful about America. And I ask you to sustain that hope. I'm not talking about blind optimism, the kind of hope that just ignores the enormity of the tasks ahead or the roadblocks that stand in our path. I'm not talking about the wishful idealism that allows us to just sit on the sidelines or shirk from a fight. 

      I have always believed that hope is that stubborn thing inside us that insists, despite all the evidence to the contrary, that something better awaits us so long as we have the courage to keep reaching, to keep working, to keep fighting. 

      America, I believe we can build on the progress we've made and continue to fight for new jobs and new opportunity and new security for the middle class. I believe we can keep the promise of our founders, the idea that if you're willing to work hard, it doesn't matter who you are or where you come from or what you look like or where you love. It doesn't matter whether you're black or white or Hispanic or Asian or Native American or young or old or rich or poor, able, disabled, gay or straight, you can make it here in America if you're willing to try. 

      I believe we can seize this future together because we are not as divided as our politics suggests. We're not as cynical as the pundits believe. We are greater than the sum of our individual ambitions, and we remain more than a collection of red states and blue states. We are and forever will be the United States of America. 

      And together with your help and God's grace we will continue our journey forward and remind the world just why it is that we live in the greatest nation on Earth. 

      Thank you, America. God bless you. God bless these United States.
      '''
      }
    r = requests.post( url, data=params )
    self.assertEqual( 200, r.status_code )
    d = json.loads( r.text )
    self.assertEqual( [u'count_keywords_stemmed', u'count_keywords_unstemmed', u'count_keywords_unstemmed_additional', u'count_words_repeating_stemmed', u'count_words_repeating_unstemmed', u'count_words_total', u'keywords_stemmed', u'keywords_unstemmed', u'keywords_unstemmed_additional', u'repeating_words_unstemmed', u'time_start', u'time_taken'], sorted(d.keys()) )
  