
=======================
hetrec2011-delicious-2k
=======================

-------
Version
-------

Version 1.0 (May 2011)

-----------
Description
-----------

    This dataset contains social networking, bookmarking, and tagging information 
    from a set of 2K users from Delicious social bookmarking system.
    http://www.delicious.com 

    The dataset is released in the framework of the 2nd International Workshop on 
    Information Heterogeneity and Fusion in Recommender Systems (HetRec 2011) 
    http://ir.ii.uam.es/hetrec2011 
    at the 5th ACM Conference on Recommender Systems (RecSys 2011)
    http://recsys.acm.org/2011 

---------------
Data statistics
---------------

    1867 users
   69226 URLs
   38581 principal URLs, e.g. www.delicious.com for http://www.delicious.com, http://www.delicious.com/tag, http://www.delicious.com/help/api
      
    7668 bi-directional user relations, i.e. 15328 (user_i, user_j) pairs
         avg. 8.236 relations per user
   
   53388 tags
  437593 tag assignments (tas), i.e. tuples [user, tag, URL]
         avg. 234.383 tas per URL
         avg. 6.321 tas per URL
  104799 bookmarks, i.e. distinct pairs [user, URL] obtained from tas
         avg. 56.132 bookmarked URLs per user
         avg. 1.514 users bookmarking a URL

-----
Files
-----

   * user_contacts.dat - user_contacts-timestamps.dat
   
   	These files contain the contact relations between users in the database.
   	
   	A contact relation is identified between two users when they belong to 
   	a mutual fan relation in Delicious.
   	
   	The files also contain the timestamps when contact relations were created in Delicious.
     
   * bookmarks.dat
   
        This file contains information about bookmarked URLs.
   
   * tags.dat
   
   	This file contains the set of tags available in the dataset.
   
   * user_taggedbookmarks.dat - user_taggedbookmarks-timestamps.dat
   
        These files contain the tag assignments of the bookmarked URLs provided by each particular user.
        
        They also contain the timestamps when the tag assignments were done.
   
   * bookmark_tags.dat
   
        This file contains the tags assigned to the bookmarked URLs, and the number of times 
        the tags were assigned to each URL.
   
-----------
Data format
-----------

   The data is formatted one entry per line as follows (tab separated, "\t"):

   * user_contacts-timestamps.dat
   
        userID \t contactID \t timestamp

        Example:
        8	28371	1286151259000

   * user_contacts.dat
   
        userID \t contactID \t date_day \t date_month \t date_year \t date_hour \t date_minute \t date_second

        Example:
        8	28371	4	10	2010	2	14	19

   * bookmarks.dat
   
        id \t md5  \t title  \t url  \t md5Principal  \t urlPrincipal

        Example:
        1	ab4954b633ddaf5b5bba6e9b71aa6b70	IFLA - The official website of the International Federation of Library Associations and Institutions	http://www.ifla.org/	7f431306c428457bc4e12b15634484f	www.ifla.org

   * tags.dat

        id \t value

        Example:
        1	collection_development
   
   * user_taggedbookmarks.dat

        userID \t bookmarkID \t tagID \t day \t month \t year \t hour \t minute \t second
        
        Example:
        8	1	1	8	11	2010	23	29	22

   * user_taggedbookmarks-timestamps.dat

        userID \t bookmarkID \t tagID \t timestamp
        
        Example:
        8	1	1	1289255362000
   
   * bookmark_tags.dat

        bookmarkID \t tagID \t tagWeight

        Example:
        1	2	276

------- 
License
-------

   The users' names and other personal information in Delicious are not provided in the dataset.

   The data contained in hetrec2011-delicious-2k.zip is made available for non-commercial use.
   
   Those interested in using the data in a commercial context should contact Delicious staff:
   http://www.delicious.com

----------------
Acknowledgements
----------------

   This work was supported by the Spanish Ministry of Science and Innovation (TIN2008-06566-C04-02), 
   and the Regional Government of Madrid (S2009TIC-1542).

----------
References
----------

   When using this dataset you should cite:
      - Delicious website, http://www.delicious.com

   You may also cite HetRec'11 workshop as follows:

   @inproceedings{Cantador:RecSys2011,
      author = {Cantador, Iv\'{a}n and Brusilovsky, Peter and Kuflik, Tsvi},
      title = {2nd Workshop on Information Heterogeneity and Fusion in Recommender Systems (HetRec 2011)},
      booktitle = {Proceedings of the 5th ACM conference on Recommender systems},
      series = {RecSys 2011},
      year = {2011},
      location = {Chicago, IL, USA},
      publisher = {ACM},
      address = {New York, NY, USA},
      keywords = {information heterogeneity, information integration, recommender systems},
   } 

-------
Credits
-------

   This dataset was built by Iván Cantador with the collaboration of Alejandro Bellogín and Ignacio Fernández-Tobías, 
   members of the Information Retrieval group at Universidad Autonoma de Madrid (http://ir.ii.uam.es)

-------   
Contact
-------

   Iván Cantador, ivan [dot] cantador [at] uam [dot] es
