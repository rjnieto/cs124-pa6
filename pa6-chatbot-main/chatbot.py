# PA6, CS124, Stanford, Winter 2019
# v.1.0.3
# Original Python code by Ignacio Cases (@cases)
######################################################################
import util

from porter_stemmer import PorterStemmer
import numpy as np


# noinspection PyMethodMayBeStatic
class Chatbot:
    """Simple class to implement the chatbot for PA 6."""

    def __init__(self, creative=False):
        # The chatbot's default name is `moviebot`.
        # TODO: Give your chatbot a new name.
        self.name = 'randi'

        self.creative = False
        # self.creative = True
        # This matrix has the following shape: num_movies x num_users
        # The values stored in each row i and column j is the rating for
        # movie i by user j
        self.titles, ratings = util.load_ratings('data/ratings.txt')
        self.sentiment = util.load_sentiment_dictionary('data/sentiment.txt')

        ########################################################################
        # TODO: Binarize the movie ratings matrix.                             #
        ########################################################################

        # Binarize the movie ratings before storing the binarized matrix.
        self.ratings = self.binarize(ratings, 2.5)

        # Create some global variables
        self.num_data_pts = 0
        self.movie_data_points = np.zeros(np.shape(self.ratings)[0])
        # Create list of affirmations later

        # Create list of affirmations later
        self.affirmations = ["yes", "yeah", "yup", "sure", "ya", "ye", "that's right", "correct", "sure"]
        self.refutations = ["no", "nah", "nope"]

        # These are all for clarification of misspelled titles
        self.is_clarifying = False
        self.clarifying_titles = []
        self.stored_sentiment = 0
        self.yes_or_no = False

        # The following is for when there are no quotes
        # in the user's input
        self.no_quotes = False
        self.user = ""
        ########################################################################
        #                             END OF YOUR CODE                         #
        ########################################################################

    ############################################################################
    # 1. WARM UP REPL                                                          #
    ############################################################################

    def greeting(self):
        """Return a message that the chatbot uses to greet the user."""
        ########################################################################
        # TODO: Write a short greeting message                                 #
        ########################################################################

        greeting_message = "What's up! I'm Randi your personal movie recommending assistant. Lets start out by identifying your movie preferences. Tell me about a movie you like or dislike."

        ########################################################################
        #                             END OF YOUR CODE                         #
        ########################################################################
        return greeting_message

    def goodbye(self):
        """
        Return a message that the chatbot uses to bid farewell to the user.
        """
        ########################################################################
        # TODO: Write a short farewell message                                 #
        ########################################################################

        goodbye_message = "This has been so much fun! See ya later..."

        ########################################################################
        #                          END OF YOUR CODE                            #
        ########################################################################
        return goodbye_message

    ############################################################################
    # 2. Modules 2 and 3: extraction and transformation                        #
    ############################################################################

    def process(self, line):
        """Process a line of input from the REPL and generate a response.
        This is the method that is called by the REPL loop directly with user
        input.
        You should delegate most of the work of processing the user's input to
        the helper functions you write later in this class.
        Takes the input string from the REPL and call delegated functions that
          1) extract the relevant information, and
          2) transform the information into a response to the user.
        Example:
          resp = chatbot.process('I loved "The Notebook" so much!!')
          print(resp) // prints 'So you loved "The Notebook", huh?'
        :param line: a user-supplied line of text
        :returns: a string containing the chatbot's response to the user input
        """
        ########################################################################
        # TODO: Implement the extraction and transformation in this method,    #
        # possibly calling other functions. Although your code is not graded   #
        # directly based on how modular it is, we highly recommended writing   #
        # code in a modular fashion to make it easier to improve and debug.    #
        ########################################################################

        if self.is_clarifying:
            # If they say no to the options
            # Move on and ask again what movies they like

            self.is_clarifying = False
            self.no_quotes = False
            if self.yes_or_no:
                self.yes_or_no = False
                if line.lower() in self.affirmations:
                    line = self.clarifying_titles[0]
                elif line.lower() in self.refutations:
                    # Do something like I'm sorry, can you please enter another movie
                    response = "I'm sorry about that, it may have been unclear. Can you please tell me about another movie or be more specific/clear?"
                    self.clarifying_titles.clear()
                    return response
                else:
                    self.is_clarifying = True
                    self.yes_or_no = True
                    response = "Is that a yes or a no?"
                    return response
            else:
                if not line.isnumeric() or int(line) >= len(self.clarifying_titles):
                    response = "Let's move past this movie...please tell me something else!"
                    self.clarifying_titles.clear()
                    return response
                line = self.clarifying_titles[int(line)]
            if self.stored_sentiment >= 1:
                line = "I liked " + "\"" + line + "\""
            else:
                line = "I did not like " + "\"" + line + "\""

            self.clarifying_titles.clear()
        # handles only one movie right now

        # if there are more than one titles for what the user gives, we have to disambiguate

        # if there are no matching titles, then we have to use find_closest
        # print(line)
        titles = util.load_titles('data/movies.txt')
        potential_title_in_line = self.extract_titles(line)  # this returns list of titles found
        # print(self.find_movies_by_title(titles[potential_title_in_line[0]][0]))
        # use find_movies_by_title
        # for x in range(len(potential_title_in_line)):
        # print(potential_title_in_line)
        response = ""
        if self.no_quotes:
            lowerLine = line.lower().split(' ')
            if lowerLine[0] in self.refutations:
                response = "Totally get that"
                return response
            if lowerLine[0] in self.affirmations:
                response = "Yeah? Mhm."
                return response
            if lowerLine[0:2] == ['i', 'am']:
                response = "Ah, must be CRAZY to be " + lowerLine[2]
                return response
            if lowerLine[0:2] == ['thank', 'you'] or lowerLine[0] == ['thanks']:
                response = "No, thank you!"
                return response
            if lowerLine[0:2] == ["what's", 'up']:
                response = "Chilling like a villain"
                return response
            if lowerLine[0:4] == ['how', 'old', 'are', 'you']:
                response = "A whopping 0 years old. What about you?"
                return response
            if lowerLine[1:3] == ['years', 'old']:
                response = "Wow that means you are " + lowerLine[0] + " years older than me!"
                return response
            if lowerLine[0:3] == ['how', 'are', 'you']:
                response = "Great! "
                return response
            if lowerLine[0:2] == ['i', 'feel']:
                response = "Ah, must be CRAZY to feel " + lowerLine[2]
                return response
            if lowerLine[0:3] == ["what's", 'your', 'name']:
                response = "Randi. Coolest name out there. "
                return response
            if lowerLine[0:3] == ['my', 'name', 'is']:
                self.user = lowerLine[3]
                response = "It's lovely to meet you " + self.user
                return response
            if lowerLine[0] == "who":
                response = "Definitely someone who is a rockstar"
                return response
            if lowerLine[0] == "what":
                response = "To be completely honest, I'm not too sure!"
                return response
            if lowerLine[0] == "where":
                response = "Probably somewhere super rural...or urban..."
                return response
            if lowerLine[0] == "when":
                response = "At a later time...don't rush it"
                return response
            if lowerLine[0] == "why":
                response = "Now that I'm thinking of it...I'm not too sure why!"
                return response
            if lowerLine[0] == "how":
                response = "Not sure!"
                return response
            if lowerLine[0] == "hi":
                response = "Hello there good fellow!"
                return response
            if lowerLine[0] == "hello":
                response = "Right back at you"
                return response
            if lowerLine[0] == "hey":
                response = "Hey there!"
                return response
            
            
            # print("london")
            if len(potential_title_in_line) == 0:
                # if empty, say try again
                response = "Sorry, I can't find any matching movie titles. Please let me know of another movie or check your spelling/accuracy."
                # self.is_clarifying = False
                self.no_quotes = False
                return response
            if len(potential_title_in_line) > 0:
                self.is_clarifying = True
                self.stored_sentiment = self.extract_sentiment(line)
                if len(potential_title_in_line) == 1:
                    self.yes_or_no = True
                    response = "Just to clarify, did you mean this movie above?"
                else:
                    response = "Hmmm, did you mean any of these movies above? (Please select number above): "
                for i in range(len(potential_title_in_line)):
                    self.clarifying_titles.append(potential_title_in_line[i])
                    if self.yes_or_no:
                        print(potential_title_in_line)
                    else:
                        print(str(i) + ". " + potential_title_in_line[i])
            return response
        # print(potential_title_in_line)
        if len(potential_title_in_line) > 0:
            potential_movies = self.find_movies_by_title(potential_title_in_line[0])  # again, for now there is only one, not dealing with multiple movies in same input

            if len(potential_movies) > 1:
                # if it's in quotes but if there's no date and there are more than 1
                self.is_clarifying = True
                self.stored_sentiment = self.extract_sentiment(line)
                # print("london")
                response = "There is more than one movie named " + potential_title_in_line[0] + "." + " Which one did you mean? (Please select number above): "
                articles = [", The", ", An", ", A"]
                for i in range(len(potential_movies)):
                    curr_title = titles[potential_movies[i]][0]
                    dateless_curr_title = curr_title[0:len(curr_title) - 7]
                    # Fix this, you have to find the comma and than compare until the end, 5 is only for ", The"
                    comma_index = dateless_curr_title.rfind(",")
                    if comma_index != -1:
                        if dateless_curr_title[comma_index:] in articles:
                            # We have to rearrange
                            first_segment = dateless_curr_title[comma_index + 2:]
                            second_segment = dateless_curr_title[0:comma_index]
                            third_segment = curr_title[len(curr_title) - 6:]
                            curr_title = first_segment + " " + second_segment + " " + third_segment
                    self.clarifying_titles.append(curr_title)
                    print(str(i) + ". " + curr_title)
                return response
            if len(potential_movies) == 0:
                # edit distance
                # this segment is clarifying based on a misspelled word
                print("You might have misspelled the title, wait a few seconds so I can fetch something you may be looking for...")
                self.is_clarifying = True
                self.stored_sentiment = self.extract_sentiment(line)
                close_titles = self.find_movies_closest_to_title(potential_title_in_line[0])
                # this is where you need to add if statement
                if len(close_titles) > 0:
                    response = "Did you mean any of the following (Please select number above): "
                    for i in range(len(close_titles)):  # currently assuming it's size of one
                        # Before appending, ensure you edit titles that start with article to
                        # be in natural format
                        curr_close_title = titles[close_titles[i]][0]
                        dateless_curr_close_title = curr_close_title[0:len(curr_close_title) - 7]
                        special_articles = [", The", ", An", ", A"]
                        comma_i = curr_close_title.rfind(",")
                        if comma_i != -1:
                            if dateless_curr_close_title[comma_i:] in special_articles:
                                first_part = dateless_curr_close_title[comma_i + 2:]
                                second_part = dateless_curr_close_title[0:comma_i]
                                third_part = curr_close_title[len(curr_close_title) - 6:]
                                curr_close_title = first_part + " " + second_part + " " + third_part
                        self.clarifying_titles.append(curr_close_title)
                        print(str(i) + ". " + curr_close_title)
                else:
                    self.is_clarifying = False
                    response = "Sorry, I can't find any matching movie titles. Please let me know of another movie or check your spelling/accuracy."
                return response

            sentiment = self.extract_sentiment(line)
            # there might be more than one, then we have to disambiguate
            list_of_indices = self.find_movies_by_title(potential_title_in_line[0])
            self.movie_data_points[list_of_indices[0]] = 1  # assuming there is only one index
            self.num_data_pts += 1
            clean_title = titles[list_of_indices[0]][0]
            dateless_clean_title = clean_title[0:len(clean_title) - 7]
            special_clean_articles = [", The", ", An", ", A"]
            comma_loc = clean_title.rfind(",")

            if comma_loc != -1:
                if dateless_clean_title[comma_loc:] in special_clean_articles:
                    part_1 = dateless_clean_title[comma_loc + 2:]
                    part_2 = dateless_clean_title[0:comma_loc]
                    part_3 = clean_title[len(clean_title) - 6:]
                    clean_title = part_1 + " " + part_2 + " " + part_3
            # May have to change values for checks in if statements
            if sentiment >= 1:

                response = "Glad you enjoyed " + clean_title + "!" + " Tell me about another movie you've seen."
                # update global
            elif sentiment == 0:
                response = "I can't tell if you liked " + clean_title + " or not."
            else:
                response = "Sorry to hear you didn't like " + clean_title + "." + " Tell me about another movie you've seen."

            if self.num_data_pts >= 5:
                rec = self.recommend(self.movie_data_points, self.ratings)
                first_rec = rec[0]
                response += "\nHere is a recommendation for you: " + titles[first_rec][0] + "\nFeel free to continue telling about your movie preferences."

        ########################################################################
        #                          END OF YOUR CODE                            #
        ########################################################################
        return response

    @staticmethod
    def preprocess(text):
        """Do any general-purpose pre-processing before extracting information
        from a line of text.
        Given an input line of text, this method should do any general
        pre-processing and return the pre-processed string. The outputs of this
        method will be used as inputs (instead of the original raw text) for the
        extract_titles, extract_sentiment, and extract_sentiment_for_movies
        methods.
        Note that this method is intentially made static, as you shouldn't need
        to use any attributes of Chatbot in this method.
        :param text: a user-supplied line of text
        :returns: the same text, pre-processed
        """
        ########################################################################
        # TODO: Preprocess the text into a desired format.                     #
        # NOTE: This method is completely OPTIONAL. If it is not helpful to    #
        # your implementation to do any generic preprocessing, feel free to    #
        # leave this method unmodified.                                        #
        ########################################################################

        ########################################################################
        #                             END OF YOUR CODE                         #
        ########################################################################

        return text

    def extract_titles(self, preprocessed_input):
        """Extract potential movie titles from a line of pre-processed text.
        Given an input text which has been pre-processed with preprocess(),
        this method should return a list of movie titles that are potentially
        in the text.
        - If there are no movie titles in the text, return an empty list.
        - If there is exactly one movie title in the text, return a list
        containing just that one movie title.
        - If there are multiple movie titles in the text, return a list
        of all movie titles you've extracted from the text.
        Example:
          potential_titles = chatbot.extract_titles(chatbot.preprocess(
                                            'I liked "The Notebook" a lot.'))
          print(potential_titles) // prints ["The Notebook"]
        :param preprocessed_input: a user-supplied line of text that has been
        pre-processed with preprocess()
        :returns: list of movie titles that are potentially in the text
        """
        extracted_titles = []
        new_substring = preprocessed_input
        curr_index = new_substring.find("\"")
        if curr_index == -1:
            # print(preprocessed_input)
            self.no_quotes = True
            titles = util.load_titles('data/movies.txt')
            articles = [", The", ", An", ", A"]
            for i in range(len(titles)):
                curr_title_date = titles[i][0]  # with year
                curr_title_no_date = curr_title_date[0:len(titles[i][0]) - 7]  # without year
                curr_article_title_date = ""
                curr_article_title_no_date = ""
                starts_with_article = False
                date = curr_title_date[len(curr_title_date) - 6:]
                comma_index = curr_title_no_date.rfind(",")
                if comma_index != -1:
                    if curr_title_no_date[comma_index:] in articles:
                        starts_with_article = True
                        # make into natural string, without and with date
                        first_segment = curr_title_no_date[comma_index + 2:]
                        second_segment = curr_title_no_date[0:comma_index]
                        curr_article_title_no_date = first_segment + " " + second_segment
                        curr_article_title_date = curr_article_title_no_date + " " + date


                if curr_title_date.lower() in preprocessed_input.lower():
                    extracted_titles.clear()
                    extracted_titles.append(curr_title_date)
                    break
                elif curr_title_no_date.lower() in preprocessed_input.lower():
                    # ensure you don't add it if same movie but with
                    # date has been added
                    # extracted_titles.append(curr_title_no_date)

                    # make sure there is a space before it and after it is either a space, colon/period/exclamation/question/comma, or is last character in string
                    # Or its the first character and there is a space after it
                    is_valid = False
                    valid_punct = [".", "!", "?", ",", ";", " "]
                    scanning_input = preprocessed_input.lower()
                    potential_index = scanning_input.find(curr_title_no_date.lower())
                    while potential_index != -1:
                        if potential_index == 0 and scanning_input[potential_index + len(curr_title_no_date)] in valid_punct:
                            is_valid = True
                            break
                        if (potential_index == len(scanning_input) - len(curr_title_no_date)) and scanning_input[potential_index - 1] == " ":
                            is_valid = True
                            break
                        if (potential_index > 0) and (potential_index + len(curr_title_no_date) != len(scanning_input)):
                            if (scanning_input[potential_index - 1] == " ") and (scanning_input[potential_index + len(curr_title_no_date)] in valid_punct):
                                is_valid = True
                                break
                        scanning_input = scanning_input[potential_index+1:]
                        potential_index = scanning_input.lower().find(curr_title_no_date.lower())
                    if is_valid:
                        extracted_titles.append(curr_title_date)
                if starts_with_article:
                    if curr_article_title_date.lower() in preprocessed_input.lower():
                        extracted_titles.clear()
                        extracted_titles.append(curr_article_title_date)
                        break
                    if curr_article_title_no_date.lower() in preprocessed_input.lower():
                        extracted_titles.append(curr_article_title_date)
        else:
            while curr_index != -1:
                new_substring = new_substring[curr_index + 1:]
                end_index = new_substring.find("\"")
                if end_index != -1:
                    extracted_titles.append(new_substring[0:end_index])
                    new_substring = new_substring[end_index + 1:]
                    curr_index = new_substring.find("\"")
                else:
                    break
        return extracted_titles

    def find_movies_by_title(self, title):
        """ Given a movie title, return a list of indices of matching movies.
        - If no movies are found that match the given title, return an empty
        list.
        - If multiple movies are found that match the given title, return a list
        containing all of the indices of these matching movies.
        - If exactly one movie is found that matches the given title, return a
        list
        that contains the index of that matching movie.
        Example:
          ids = chatbot.find_movies_by_title('Titanic')
          print(ids) // prints [1359, 2716]
        :param title: a string containing a movie title
        :returns: a list of indices of matching movies
        """
        ###############################################
        # Might have to make this function so that it's
        # not case sensitive (convert to lowercase when
        # comparing). I had to do that for the function
        # find_movies_closest_to_title, so we may have
        # to implement it here to be safe.
        ###############################################
        titles = util.load_titles('data/movies.txt')
        matches = []
        # print(titles)
        edited_title = ""
        articles = [", The", ", An", ", A"]
        ######
        has_date = False
        if title[-1] == ")":
            has_date = True

        for i in range(len(titles)):
            curr_title = titles[i][0]
            curr_title_no_date = curr_title[0:len(curr_title) - 7]
            comma_index = curr_title_no_date.rfind(",")
            if comma_index != -1:
                if curr_title_no_date[comma_index:] in articles:
                    first_segment = curr_title_no_date[comma_index + 2:]
                    second_segment = curr_title_no_date[0:comma_index]
                    third_segment = curr_title[len(curr_title) - 6:]
                    if has_date:
                        curr_title = first_segment + " " + second_segment + " " + third_segment
                    else:
                        curr_title = first_segment + " " + second_segment
                else:
                    if not has_date:
                        curr_title = curr_title_no_date
            else:
                if not has_date:
                    curr_title = curr_title_no_date


            if title.lower() == curr_title.lower() or title.lower() == curr_title_no_date:
                # found exact match, so you don't need to look for more
                matches.append(i)
            else:
                title_lower = title.lower()
                curr_title_lower = curr_title_no_date.lower()
                is_valid = False
                valid_punct = [".", "!", "?", ",", ";", ":", " "]
                scanning_input = curr_title_lower
                potential_index = scanning_input.find(title_lower)
                while potential_index != -1:
                    if (potential_index == 0) and ((potential_index + len(title_lower) == len(scanning_input)) or (scanning_input[potential_index + len(title_lower)] in valid_punct)):
                        is_valid = True
                        break
                    if (potential_index == len(scanning_input) - len(title_lower)) and (scanning_input[potential_index - 1] == " "):
                        is_valid = True
                        break
                    if (potential_index > 0) and (potential_index + len(title_lower) != len(scanning_input)):
                        if (scanning_input[potential_index - 1] == " ") and (scanning_input[potential_index + len(title_lower)] in valid_punct):
                            is_valid = True
                            break
                    potential_index = scanning_input.lower().find(title_lower, potential_index + 1)
                if is_valid:
                    matches.append(i)
        return matches

    def extract_sentiment(self, preprocessed_input):
        """Extract a sentiment rating from a line of pre-processed text.
        You should return -1 if the sentiment of the text is negative, 0 if the
        sentiment of the text is neutral (no sentiment detected), or +1 if the
        sentiment of the text is positive.
        As an optional creative extension, return -2 if the sentiment of the
        text is super negative and +2 if the sentiment of the text is super
        positive.
        Example:
          sentiment = chatbot.extract_sentiment(chatbot.preprocess(
                                                    'I liked "The Titanic"'))
          print(sentiment) // prints 1
        :param preprocessed_input: a user-supplied line of text that has been
        pre-processed with preprocess()
        :returns: a numerical value for the sentiment of the text
        """

        # print("\n")
        # make a tokenizer
        str = preprocessed_input
        words = [""]
        j = 0
        # to separate these forms of punctuation
        delimiters = ['"', '"', ',', '.']
        for i in range(len(str)):
            if str[i] in delimiters:
                if words[j] == "":
                    words[j] = str[i]
                    j += 1
                else:
                    words.append(str[i])
                    j += 2
                if i != len(str) - 1:
                    words.append("")
                # print("Done \n\n")
            elif str[i] != ' ':
                words[j] += str[i]
            else:
                if words[j] != "":
                    words.append("")
                    j += 1
        # list of words done

        # sentiment evaluation
        total = 0
        # negation coefficient
        coe = 1
        negation_words = ["don't", "didn't", "never", "not", "isn't", "doesn't", "wasn't", "shouldn't", "wouldn't", "won't",
                          "can't", "couldn't", "nothing", "nobody", "hadn't", "dislike", "didnt", "isnt", "doesnt", "wasnt",
                          "shouldnt", "wouldnt", "wont","cant", "couldnt", "dont"]
        amplifiers = ["really", "reeally", "reaally", "super", "suuper", "suuuper", "dreadfully", "totally", "tootally", "never", "passionately", "desperately", "genuinely", "undoubtedly", "truly",
                      "honestly"]
        stronger_words = ["love", "terrible", "great", "fantastic", "horrible", "abysmal", "atrocious", "appalling", "hate", "vile", "deplorable",
                          "appreciate", "passionate", "enjoy"]
        factor = 1
        movie_title = False
        stemmer = PorterStemmer()
        for word in words:
            # negation words flip sentiment meaning
            if word in negation_words and movie_title == False:
                coe = -1
            # so the words in the movie dont influence overall text sentiment
            if (word in stronger_words or word in amplifiers) and movie_title == False:
                factor = 2
            elif word == '"' or word == '"':
                # switch to false if previously true
                if movie_title:
                    movie_title = False
                # switch to true if previously false
                else:
                    movie_title = True

            if word in self.sentiment and not movie_title:
                sent = self.sentiment[word]
                # add to total and multiply by negation coefficient
                if sent == "pos":
                    total += 1 * coe * factor
                if sent == "neg":
                    total += -1 * coe * factor

            else:
                word2 = stemmer.stem(word, 0, len(word) - 1)
                # doesnt stem enjoy correctly because who knows
                if (word2 in stronger_words or word2 in amplifiers) and movie_title == False:
                    factor = 2
                if word2 == "enjoi":
                    word2 = "enjoy"
                # print(word2)
                if word2 in self.sentiment and not movie_title:
                    sent = self.sentiment[word2]
                    # add to total and multiply by negation coefficient
                    if sent == "pos":
                        total += 1 * coe * factor
                    if sent == "neg":
                        total += -1 * coe * factor
        # print("Word List: ", words)
        # print("Sentiment Score: ", total)
        return total

    def tokenize(self, preprocessed_input):
        str = preprocessed_input
        words = [""]
        j = 0
        # to separate these forms of punctuation
        movie_title = False
        delimiters = [',', '.']
        movie_delimiters = ['"', '"']
        for i in range(len(str)):
            if str[i] in movie_delimiters:
                if movie_title:
                    movie_title = False
                    words[j] += str[i]
                    words.append("")
                    j += 1
                else:
                    movie_title = True
                    words[j] += str[i]

            else:
                if movie_title:
                    words[j] += str[i]
                else:
                    if str[i] in delimiters:
                        if words[j] == "":
                            words[j] = str[i]
                            j += 1
                        else:
                            words.append(str[i])
                            j += 2
                        if i != len(str) - 1:
                            words.append("")
                            # print("Done \n\n")
                    elif str[i] != ' ':
                        words[j] += str[i]
                    else:
                        if words[j] != "":
                            words.append("")
                            j += 1
        # list of words done

        return words

    def extract_sentiment_for_movies(self, preprocessed_input):
        """Creative Feature: Extracts the sentiments from a line of
        pre-processed text that may contain multiple movies. Note that the
        sentiments toward the movies may be different.
        You should use the same sentiment values as extract_sentiment, described
        above.
        Hint: feel free to call previously defined functions to implement this.
        Example:
          sentiments = chatbot.extract_sentiment_for_text(
                           chatbot.preprocess(
                           'I liked both "Titanic (1997)" and "Ex Machina".'))
          print(sentiments) // prints [("Titanic (1997)", 1), ("Ex Machina", 1)]
        :param preprocessed_input: a user-supplied line of text that has been
        pre-processed with preprocess()
        :returns: a list of tuples, where the first item in the tuple is a movie
        title, and the second is the sentiment in the text toward that movie
        """
        # print("\n")
        words = self.tokenize(preprocessed_input)
        # print(words)

        movies = []
        movie_count = 0
        # sentiment evaluation
        total = 0
        # negation coefficient
        coe = 1
        negation_words = ["don't", "didn't", "never", "not", "isn't", "doesn't", "wasn't", "shouldn't", "wouldn't", "won't",
                          "can't", "couldn't", "nothing", "nobody", "hadn't"]
        stemmer = PorterStemmer()
        switch_before_end = False
        for word in words:
            # negation words flip sentiment meaning
            if word == '.' and switch_before_end:
                name = ""
                points = 0
                for key, val in movies[len(movies) - 1].items():
                    name = key
                    points = val
                points = total * coe
                movies[len(movies) - 1].update({name: points})
            if word in negation_words:
                coe = coe * -1
            # so the words in the movie dont influence overall text sentiment
            elif word[0] == '"' or word[0] == '"':
                # switch to false if previously true
                movies.append({word[1:len(word) - 1]: total * coe})
                switch_before_end = False
                # print("switch before end", switch_before_end)
                movie_count += 1

            if word in self.sentiment:
                sent = self.sentiment[word]
                # add to total and multiply by negation coefficient
                if sent == "pos":
                    total = 1
                    switch_before_end = True
                    # print("switch before end", switch_before_end)
                if sent == "neg":
                    total = -1

            else:
                word2 = stemmer.stem(word, 0, len(word) - 1)
                # doesnt stem enjoy correctly because who knows
                if word2 == "enjoi":
                    word2 = "enjoy"
                # print(word2)
                if word2 in self.sentiment:
                    sent = self.sentiment[word2]
                    # add to total and multiply by negation coefficient
                    if sent == "pos":
                        total += 1 * coe
                    if sent == "neg":
                        total += -1 * coe

        tuple_list = []
        for i in range(len(movies)):
            for key, val in movies[i].items():
                tuple_list.append((key, val))

        return tuple_list

    def find_movies_closest_to_title(self, title, max_distance=3):
        """Creative Feature: Given a potentially misspelled movie title,
        return a list of the movies in the dataset whose titles have the least
        edit distance from the provided title, and with edit distance at most
        max_distance.
        - If no movies have titles within max_distance of the provided title,
        return an empty list.
        - Otherwise, if there's a movie closer in edit distance to the given
        title than all other movies, return a 1-element list containing its
        index.
        - If there is a tie for closest movie, return a list with the indices
        of all movies tying for minimum edit distance to the given movie.
        Example:
          # should return [1656]
          chatbot.find_movies_closest_to_title("Sleeping Beaty")
        :param title: a potentially misspelled title
        :param max_distance: the maximum edit distance to search for
        :returns: a list of movie indices with titles closest to the given title
        and within edit distance max_distance
        """

        titles = util.load_titles('data/movies.txt')
        matches_and_distance = []

        articles = [", The", ", An", ", A"]
        user_input_title = title
        has_date = False
        if user_input_title[len(user_input_title) - 1] == ")":
            has_date = True
        for i in range(len(titles)):
            current_title = titles[i][0]  # target
            # check whether the title has article first or not, because not
            # all do the weird title thing
            source = user_input_title
            curr_title_no_date = current_title[0:len(current_title) - 7]
            comma_index = curr_title_no_date.rfind(",")
            if has_date:
                # create current_title in format with date
                if comma_index != -1:
                    if curr_title_no_date[comma_index:] in articles:
                        # split into segments and arrange with date
                        segment_1 = curr_title_no_date[comma_index + 2:]
                        segment_2 = curr_title_no_date[0:comma_index]
                        segment_3 = current_title[len(current_title) - 6:]
                        current_title = segment_1 + " " + segment_2 + " " + segment_3
            else:
                # create current_title in format without date
                if comma_index != -1:
                    if curr_title_no_date[comma_index:] in articles:
                        # split into segments and arrange with date
                        segment_1 = curr_title_no_date[comma_index + 2:]
                        segment_2 = curr_title_no_date[0:comma_index]
                        current_title = segment_1 + " " + segment_2
                    else:
                        current_title = curr_title_no_date
                else:
                    current_title = curr_title_no_date

            # for testing purposes
            # current_title = "Ten"
            # source = "Te"
            # build matrix
            target_list = []
            for c_t in range(len(current_title)):
                target_list.append(current_title[c_t].lower())
            source_list = []
            for c_s in range(len(source)):
                source_list.append(source[c_s].lower())

            # set initial row and column
            matrix = np.zeros((len(source_list) + 1, len(target_list) + 1))
            for c in range(len(target_list) + 1):
                matrix[0][c] = c

            for r in range(len(source_list) + 1):
                matrix[r][0] = r

            # loop through all of the rows and columns and
            # update value in current
            for row in range(1, len(source_list) + 1):
                for col in range(1, len(target_list) + 1):
                    potential_values = []
                    potential_values.append(matrix[row - 1][col] + 1)
                    potential_values.append(matrix[row][col - 1] + 1)
                    if target_list[col - 1] == source_list[row - 1]:
                        potential_values.append(matrix[row - 1][col - 1])
                    else:
                        potential_values.append(matrix[row - 1][col - 1] + 2)
                    matrix[row][col] = min(potential_values)

            min_edit_distance = matrix[len(source_list)][len(target_list)]
            if min_edit_distance <= max_distance:
                if len(matches_and_distance) == 0:
                    matches_and_distance.append((i, min_edit_distance))
                else:
                    if min_edit_distance == matches_and_distance[0][1]:
                        matches_and_distance.append((i, min_edit_distance))
                    if min_edit_distance < matches_and_distance[0][1]:
                        matches_and_distance.clear()
                        matches_and_distance.append((i, min_edit_distance))
            # for testing
        matching_indices = []
        for tup in matches_and_distance:
            matching_indices.append(tup[0])

        return matching_indices

    def disambiguate(self, clarification, candidates):
        """Creative Feature: Given a list of movies that the user could be
        talking about (represented as indices), and a string given by the user
        as clarification (eg. in response to your bot saying "Which movie did
        you mean: Titanic (1953) or Titanic (1997)?"), use the clarification to
        narrow down the list and return a smaller list of candidates (hopefully
        just 1!)
        - If the clarification uniquely identifies one of the movies, this
        should return a 1-element list with the index of that movie.
        - If it's unclear which movie the user means by the clarification, it
        should return a list with the indices it could be referring to (to
        continue the disambiguation dialogue).
        Example:
          chatbot.disambiguate("1997", [1359, 2716]) should return [1359]
        :param clarification: user input intended to disambiguate between the
        given movies
        :param candidates: a list of movie indices
        :returns: a list of indices corresponding to the movies identified by
        the clarification
        """
        titles = util.load_titles('data/movies.txt')
        # Clarification is a year
        isLatest = False
        latest = 0
        latestIndex = 0
        for index in candidates:
            movie = titles[index]
            if "recent" in clarification:
                isLatest = True
            ind = movie[0].find("(")
            year = movie[0][ind + 1: ind + 5]
            if str(year) > str(latest):
                latest = year
                latestIndex = index
            if clarification in movie[0]:
                return [index]

        if isLatest:
            return [latestIndex]
        return candidates

    ############################################################################
    # 3. Movie Recommendation helper functions                                 #
    ############################################################################

    @staticmethod
    def binarize(ratings, threshold=2.5):
        """Return a binarized version of the given matrix.
        To binarize a matrix, replace all entries above the threshold with 1.
        and replace all entries at or below the threshold with a -1.
        Entries whose values are 0 represent null values and should remain at 0.
        Note that this method is intentionally made static, as you shouldn't use
        any attributes of Chatbot like self.ratings in this method.
        :param ratings: a (num_movies x num_users) matrix of user ratings, from
         0.5 to 5.0
        :param threshold: Numerical rating above which ratings are considered
        positive
        :returns: a binarized version of the movie-rating matrix
        """
        ########################################################################
        # TODO: Binarize the supplied ratings matrix.                          #
        #                                                                      #
        # WARNING: Do not use self.ratings directly in this function.          #
        ########################################################################

        # The starter code returns a new matrix shaped like ratings but full of
        # zeros.
        binarized_ratings = np.zeros_like(ratings)
        for i in range(len(ratings)):
            for j in range(len(ratings[0])):
                if ratings[i][j] > threshold:
                    binarized_ratings[i][j] = 1
                elif ratings[i][j] <= threshold:
                    binarized_ratings[i][j] = -1
                if ratings[i][j] == 0:
                    binarized_ratings[i][j] = 0

        ########################################################################
        #                        END OF YOUR CODE                              #
        ########################################################################
        return binarized_ratings

    def similarity(self, u, v):
        """Calculate the cosine similarity between two vectors.
        You may assume that the two arguments have the same shape.
        :param u: one vector, as a 1D numpy array
        :param v: another vector, as a 1D numpy array
        :returns: the cosine similarity between the two vectors
        """
        ########################################################################
        # TODO: Compute cosine similarity between the two vectors.             #
        ########################################################################
        num = np.dot(u, v)
        # dem = np.sqrt(np.dot(u, u)) * np.sqrt(np.dot(v, v))

        uNorm = np.linalg.norm(u)
        vNorm = np.linalg.norm(v)
        dem = uNorm * vNorm
        if dem == 0:
            return 0
        similarity = num / dem
        ########################################################################
        #                          END OF YOUR CODE                            #
        ########################################################################
        return similarity

    def normalize(self, matrix):
        magnitude_r = np.sum(matrix * matrix, axis=1) ** 0.5
        # this stops zero division
        magnitude_r = np.maximum(magnitude_r, np.array(1e-20))
        return matrix / magnitude_r[:, np.newaxis]

    def recommend(self, user_ratings, ratings_matrix, k=10, creative=False):
        """Generate a list of indices of movies to recommend using collaborative
         filtering.
        You should return a collection of `k` indices of movies recommendations.
        As a precondition, user_ratings and ratings_matrix are both binarized.
        Remember to exclude movies the user has already rated!
        Please do not use self.ratings directly in this method.
        :param user_ratings: a binarized 1D numpy array of the user's movie
            ratings
        :param ratings_matrix: a binarized 2D numpy matrix of all ratings, where
          `ratings_matrix[i, j]` is the rating for movie i by user j
        :param k: the number of recommendations to generate
        :param creative: whether the chatbot is in creative mode
        :returns: a list of k movie indices corresponding to movies in
        ratings_matrix, in descending order of recommendation.
        """

        ########################################################################
        # TODO: Implement a recommendation function that takes a vector        #
        # user_ratings and matrix ratings_matrix and outputs a list of movies  #
        # recommended by the chatbot.                                          #
        #                                                                      #
        # WARNING: Do not use the self.ratings matrix directly in this         #
        # function.                                                            #
        #                                                                      #
        # For starter mode, you should use item-item collaborative filtering   #
        # with cosine similarity, no mean-centering, and no normalization of   #
        # scores.                                                              #
        ########################################################################

        # Populate this list with k movie indices to recommend to the user.

        recs = []

        rated_movies = ratings_matrix[user_ratings != 0, :]
        rated_movies = self.normalize(rated_movies)
        ratings_matrix = self.normalize(ratings_matrix)
        sim_matrix = np.dot(ratings_matrix, np.transpose(rated_movies))
        ratings = user_ratings[user_ratings != 0]
        scores_array = np.dot(sim_matrix, ratings)
        scores_array = np.reshape(scores_array, (-1))
        # descneding order
        sorted_indexes = np.argsort(scores_array)[::-1]
        for ind in sorted_indexes:
            if user_ratings[ind] != 0:
                continue
            else:
                recs.append(ind)
            if len(recs) == k:
                break

        ########################################################################
        #                        END OF YOUR CODE                              #
        ########################################################################
        return recs

    ############################################################################
    # 4. Debug info                                                            #
    ############################################################################

    def debug(self, line):
        """
        Return debug information as a string for the line string from the REPL
        NOTE: Pass the debug information that you may think is important for
        your evaluators.
        """
        debug_info = 'debug info'
        return debug_info

    ############################################################################
    # 5. Write a description for your chatbot here!                            #
    ############################################################################
    def intro(self):
        """Return a string to use as your chatbot's description for the user.
        Consider adding to this description any information about what your
        chatbot can do and how the user can interact with it.
        """
        return """
        Your task is to implement the chatbot as detailed in the PA6
        instructions.
        Remember: in the starter mode, movie names will come in quotation marks
        and expressions of sentiment will be simple!
        TODO: Write here the description for your own chatbot!
        """


if __name__ == '__main__':
    print('To run your chatbot in an interactive loop from the command line, '
          'run:')
    print('    python3 repl.py')
