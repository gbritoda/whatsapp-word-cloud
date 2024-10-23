# whatsapp-word-cloud

Just created this as a joke and it's actually a very interesting experiment.

Go to any whatsapp conversation you wish to do this, click the kebab menu (3 vertical dots) and select *export* (Might not work for whatsapp web).

Save the conversation log somewhere and use the script accordingly.

`./word-cloud your_conversation.txt`

You can even filter to a user and get that user profile:

`./word-cloud convo.txt --user "John Doe"`

And change up languages, this is just to filter out filler words like "and", "the", etc. This filter comes from the `nltk` package but there's some extra work done to filter out common typos on internet speak as well like "theyre".

Default language is english

`./word-cloud convo.txt --user "John Doe" --language portuguese`
