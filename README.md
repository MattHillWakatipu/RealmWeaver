# RealmWeaver

The following is an Excerpt from the paper Hallucinating Machines.

## Method

For our final experiment, we continued to use the Critical Making methodology
for prototyping and building a system informed by our previous experiments. We
developed RealmWeaver, a collaborative tool for generating content referential to past
experiences, further investigating the efficacy of combining language models with
vector databases. This research aimed to explore the potential of the state-of-the-art
language model GPT-4 when imbued with additional long-term memory capabilities,
leveraging them for various applications, such as worldbuilding for authors. By using
the Critical Making methodology to reflect on the created artifacts, we explored these
types of systems' safety and ethical implications.

We opted to utilise Weaviate (Dilocker et al., 2016/2023), an open-source vector
database, to facilitate collaborative worldbuilding. Unlike in our previous experiment,
where the vector database was stored locally, we instead used Weaviate Cloud Services
(Weaviate - Vector Database, n.d.), a fully managed SaaS service to streamline the
management and retrieval of data from the vector database. Interaction with Weaviate
was conducted through the API using the Weaviate Python Client (Weaviate Python
Client, 2019/2023) Library.

We developed a pipeline to handle incoming requests, including pre-processing,
database retrieval, query enhancement, and model interaction. During the preprocessing
stage, we analysed what additional context was necessary based on the
incoming query and used Weaviate to find the most relevant entries within our vector
database. These entries enhanced the query, providing additional context for the
language model to draw upon during question answering.

We designed a pre-processing methodology to generate interesting and
contextually relevant responses and devised a method of automated categorisation for
referencing past experiences. We tested different data chunking strategies to manage
the length of vector database items, both from model responses and to enable the
construction of vector databases from pre-existing documents. To test the potential of
web deployment, we created a minimal web interface with Flask (Flask, 2010/2023), a
microframework for building web applications in Python.

We assessed the quality and relevance of the generated responses based on
predefined criteria derived from our previous experiments and evaluation frameworks,
both manually and with the model-graded approach. The evaluation assessed the
system's ability to recall past experiences, generate contextually relevant content, and
facilitate collaborative worldbuilding experiences for diverse user groups.

Following this method, we aimed to demonstrate the practical implementation of
language models with long-term memory capabilities through vector databases. The
findings from this experiment can provide insights into future applications of
generative models and their potential to empower a wide range of domains, from
functional to creative.

## Results

In this experiment, it was found that generating a list of topics based on an initial
query aided the model in crafting responses connected to various parts of the world.
The extraction of concepts from a user’s request string resulted in short lists of topics
closely aligned with the initial query. By utilising these topics, the system demonstrated
the ability to search the vector database for highly relevant background information and
include it in the final prompt.

The non-deterministic nature of the pre-processing stage meant that the background
context prompt altered slightly between runs, leading to some variation. However,
similar context was included in subsequent runs. This resulted in responses that, while
not blatantly contradictory, expressed some disagreement with one another.

Furthermore, during some runs, the model would occasionally encounter
repetitive patterns where identical context were included, causing it to continually
generate information surrounding a specific event. This behaviour may be
advantageous in ensuring events are well-developed but can hinder the creation of
entirely new content. It might be possible to overcome this issue using prompt
engineering, directing the model to create events unrelated to existing ones.

The chunking strategies employed in this experiment successfully divided larger
responses into smaller parts but led to fragmented and incomplete ideas being
incorporated into the vector database, even when whole paragraphs were included.
Consequently, we removed the chunking strategies and stored entire responses instead.

These results displayed a solid foundational ability for worldbuilding for the
system, as the generated responses successfully referenced multiple existing
background contexts and built upon them coherently. The system demonstrated
competence in elaborating on the given contexts and incorporating them into engaging
and cohesive narratives.

## Discussion

The initial system utilised recursive chunking, where the program was given a
hierarchy of tokens to split on, including paragraph breaks, newlines or periods, and
tried to create chunks of consistent size using the most favourable token. This method
performed exceedingly well, resulting in responses that were separated in logical
places, typically always by paragraph breaks. Despite this, it was discovered that the
separation of these responses resulted in a significant loss of structure and cohesion due
to the lack of semantic analysis during splitting.

While our initial solution, to remove chunking altogether, clearly functions, the
inclusion of larger texts could hamper the performance of the vector search. This would
likely occur due to the increased token size permitting more generalised entries. These
generalised entries are also somewhat expected, given that the background context
system functions by providing the model with varied but beneficial content.

Another potential solution would be to utilise summarisation to distil responses
to a manageable and appropriate size for storing and searching in the vector database.
This approach also comes with many issues, as summarisation constitutes a loss of
information, drastically reducing the benefits of AI-assisted content generation.
Avoiding this would require the complete response being saved in addition to the
summarisation and only searching based on the summarisation. While this would
theoretically work, any differences between these two would culminate in a less
accurate vector search.

However, the accuracy of the vector search may not be as crucial as it typically
would be due to the creative nature of the application. A considerable amount of
variance is already introduced during the calculation of beneficial concepts during 
preprocessing. Ideally, we return the most related items to these topics, but we could
suggest that the failure to do so would still provide helpful background information for
the system. We could envision intentionally including one or two unrelated entries to
encourage experimentation. As such, we felt it best to remove the chunking strategies.

It should be noted, however, that chunking would still be viable for other
applications, particularly those that necessitate large amounts of text being parsed and
vectorised. Even the relatively naïve method of recursive splitting would be helpful in
the initial creation of vector databases from existing text. Two examples of these would
be parsing and vectorising an existing work of fiction or creating a vector database
based on internal documentation for companies.

As the vector database is not locally hosted, this opens the potential for
collaborative projects. Whether it be collaborative writing projects or the previously
mentioned documentation for companies. Though the current architecture would
suffice, the lack of content moderation could easily prove troublesome on larger scales.
One particularly interesting way of handling these issues would be to take inspiration
from DAOs and democratise the approval of entry into the vector database via voting.
This move towards decentralised governance would necessitate exploring governance
mechanisms to ensure fair representation and create voting schemes that incentivise
activity within the community (Sims, 2021).

Perhaps the most significant limitation of this system is that contradictory
information may occur, as seen in testing. This is a complex problem to solve efficiently
in a purely automated manner. In a naïve implementation, checking even a single
response would be prohibitively expensive as one would have to check the response for
contradictions with each item in the vector database. More sophisticated systems could
utilise summarisation to compress the information of each item in the vector database.
This would significantly reduce overheads for checking contradictions, but as before,
any information loss from these processes could result in contradictory information
being included regardless. Manual inspection of responses for contradictions is likely
not a valid solution either, as even a relatively small project may constitute hundreds of
database entries.

However, another viewpoint on this matter is that the inclusion of slightly
contradictory responses could be utilised to represent diverse opinions on the history of
the world. This could add significant depth, complexity and verisimilitude to the work.
This would need to be treated with caution, as the individual responses would lack any
tagging indicating a specific viewpoint that the piece is from. With this in mind, only
major contradictions are likely to cause serious problems; therefore, we can assume that
an invested user or the collective user base would identify problematic responses and
disallow their entry into the database.

Overall, the RealmWeaver system demonstrates the efficacy of utilising AI
assistance for creative tasks, in this instance, aiding with worldbuilding for aspiring
novelists by augmenting generative language models with long-term memory. This
approach allows the model to create more contextually meaningful content and
significantly prevents the tendency for language models to create generic or otherwise
bland content. This system substantially lowers the skill floor required to develop
coherent, distinctive and exciting worlds while also providing a powerful tool for
competent storytellers, either as a tool for sparking inspiration or through the rapid
development of ideas.
