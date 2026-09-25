## Query 1: SELECT * FROM books WHERE in_stock = 1 AND price_gbp < 40 ORDER BY price_gbp DESC;

```sql
Empty DataFrame
Columns: [title, price_gbp, category_name]
Index: []
```

Empty DataFrame
Columns: [title, price_gbp, category_name]
Index: []


## Query 2: SELECT title, price_inr FROM books ORDER BY price_inr DESC LIMIT 10;

```sql
                                                                                            title price_inr category_name
                                                                          It's Only the Himalayas      None      Travel 2
                               Full Moon over Noahâs Ark: An Odyssey to Mount Ararat and Beyond      None      Travel 2
                               See America: A Celebration of Our National Parks & Treasured Sites      None      Travel 2
                              Vagabonding: An Uncommon Guide to the Art of Long-Term World Travel      None      Travel 2
                                                                             Under the Tuscan Sun      None      Travel 2
                                                                               A Summer In Europe      None      Travel 2
                                                                         The Great Railway Bazaar      None      Travel 2
                                                                 A Year in Provence (Provence #1)      None      Travel 2
The Road to Little Dribbling: Adventures of an American in Britain (Notes From a Small Island #2)      None      Travel 2
                                                        Neither Here nor There: Travels in Europe      None      Travel 2
```

                                                                                            title price_inr category_name
                                                                          It's Only the Himalayas      None      Travel 2
                               Full Moon over Noahâs Ark: An Odyssey to Mount Ararat and Beyond      None      Travel 2
                               See America: A Celebration of Our National Parks & Treasured Sites      None      Travel 2
                              Vagabonding: An Uncommon Guide to the Art of Long-Term World Travel      None      Travel 2
                                                                             Under the Tuscan Sun      None      Travel 2
                                                                               A Summer In Europe      None      Travel 2
                                                                         The Great Railway Bazaar      None      Travel 2
                                                                 A Year in Provence (Provence #1)      None      Travel 2
The Road to Little Dribbling: Adventures of an American in Britain (Notes From a Small Island #2)      None      Travel 2
                                                        Neither Here nor There: Travels in Europe      None      Travel 2


## Query 3: SELECT title, price_gbp FROM books ORDER BY price_gbp ASC LIMIT 5;

```sql
                                                              title price_gbp
                                            It's Only the Himalayas      None
 Full Moon over Noahâs Ark: An Odyssey to Mount Ararat and Beyond      None
 See America: A Celebration of Our National Parks & Treasured Sites      None
Vagabonding: An Uncommon Guide to the Art of Long-Term World Travel      None
                                               Under the Tuscan Sun      None
```

                                                              title price_gbp
                                            It's Only the Himalayas      None
 Full Moon over Noahâs Ark: An Odyssey to Mount Ararat and Beyond      None
 See America: A Celebration of Our National Parks & Treasured Sites      None
Vagabonding: An Uncommon Guide to the Art of Long-Term World Travel      None
                                               Under the Tuscan Sun      None


## Query 4: SELECT DISTINCT category_name FROM categories ORDER BY category_name;

```sql
       category_name
          Classics 6
Historical-Fiction 4
           Mystery 3
        Philosophy 7
           Romance 8
    Sequential-Art 5
            Travel 2
    Womens-Fiction 9
```

       category_name
          Classics 6
Historical-Fiction 4
           Mystery 3
        Philosophy 7
           Romance 8
    Sequential-Art 5
            Travel 2
    Womens-Fiction 9


## Query 5: SELECT title, category_id FROM books WHERE category_id IN (1, 2, 3) ORDER BY title;

```sql
                                                                        title        category_name
                                          1st to Die (Women's Murder Club #1)            Mystery 3
                                      A Flight of Arrows (The Pathfinders #2) Historical-Fiction 4
                                                             A Murder in Time            Mystery 3
                                                            A Paris Apartment Historical-Fiction 4
                            A Spy's Devotion (The Regency Spies of London #1) Historical-Fiction 4
                                      A Study in Scarlet (Sherlock Holmes #1)            Mystery 3
                                       A Time of Torment (Charlie Parker #14)            Mystery 3
                    Alice in Wonderland (Alice's Adventures in Wonderland #1)           Classics 6
                                                     And Then There Were None           Classics 6
                                                                  Animal Farm           Classics 6
                                                                      Beowulf           Classics 6
                                                       Between Shades of Gray Historical-Fiction 4
                                         Blood Defense (Samantha Brinkman #1)            Mystery 3
                                                Boar Island (Anna Pigeon #19)            Mystery 3
                                                                      Candide           Classics 6
                                          Career of Evil (Cormoran Strike #3)            Mystery 3
                             Delivering the Truth (Quaker Midwife Mystery #1)            Mystery 3
                                                                         Emma           Classics 6
                                           Extreme Prey (Lucas Davenport #26)            Mystery 3
    Forever and Forever: The Courtship of Henry Longfellow and Fanny Appleton Historical-Fiction 4
                                                    Girl With a Pearl Earring Historical-Fiction 4
                                                        Girl in the Blue Coat Historical-Fiction 4
                              Glory over Everything: Beyond The Kitchen House Historical-Fiction 4
                                                           Gone with the Wind           Classics 6
                                                   Hide Away (Eve Duncan #20)            Mystery 3
                                                         In a Dark, Dark Wood            Mystery 3
                                        In the Woods (Dublin Murder Squad #1)            Mystery 3
                                                                  Lilac Girls Historical-Fiction 4
                                               Little Women (Little Women #1)           Classics 6
                                                        Lost Among the Living Historical-Fiction 4
                                                         Love, Lies and Spies Historical-Fiction 4
                                                                  Most Wanted            Mystery 3
                                                                 Mrs. Houdini Historical-Fiction 4
                        Murder at the 42nd Street Library (Raymond Ambler #1)            Mystery 3
                                                              Of Mice and Men           Classics 6
                                                            Playing with Fire            Mystery 3
                                             Poisonous (Max Revere Novels #3)            Mystery 3
                                                        Sense and Sensibility           Classics 6
                                                                Sharp Objects            Mystery 3
                                                                     Starlark Historical-Fiction 4
                                         Tastes Like Fear (DI Marnie Rome #3)            Mystery 3
                                       That Darkness (Gardiner and Renner #1)            Mystery 3
     The Bachelor Girl's Guide to Murder (Herringford and Watts Mysteries #1)            Mystery 3
The Complete Stories and Poems (The Works of Edgar Allan Poe [Cameo Edition])           Classics 6
                                   The Constant Princess (The Tudor Court #1) Historical-Fiction 4
                                    The Cuckoo's Calling (Cormoran Strike #1)            Mystery 3
                                                                   The Exiled            Mystery 3
                                    The Girl In The Ice (DCI Erika Foster #1)            Mystery 3
                                                            The Girl You Lost            Mystery 3
                            The Guernsey Literary and Potato Peel Pie Society Historical-Fiction 4
                           The Hound of the Baskervilles (Sherlock Holmes #5)           Classics 6
                                                        The House by the Lake Historical-Fiction 4
                                                       The Invention of Wings Historical-Fiction 4
                                               The Last Mile (Amos Decker #2)            Mystery 3
                                             The Last Painting of Sara de Vos Historical-Fiction 4
                                                            The Little Prince           Classics 6
                                                    The Marriage of Opposites Historical-Fiction 4
                                                            The Metamorphosis           Classics 6
                              The Murder of Roger Ackroyd (Hercule Poirot #4)            Mystery 3
                          The Mysterious Affair at Styles (Hercule Poirot #1)            Mystery 3
       The No. 1 Ladies' Detective Agency (No. 1 Ladies' Detective Agency #1)            Mystery 3
                                                        The Passion of Dolssa Historical-Fiction 4
                                                          The Past Never Ends            Mystery 3
                                                   The Picture of Dorian Gray           Classics 6
                                                       The Pilgrim's Progress           Classics 6
                                                                 The Red Tent Historical-Fiction 4
                                                            The Secret Garden           Classics 6
                                                            The Secret Healer Historical-Fiction 4
                                            The Silkworm (Cormoran Strike #2)            Mystery 3
                                                    The Story of Hong Gildong           Classics 6
                                                                    The Widow            Mystery 3
                                                           Tipping the Velvet Historical-Fiction 4
                                                       Voyager (Outlander #3) Historical-Fiction 4
            What Happened on Beale Street (Secrets of the South Mysteries #2)            Mystery 3
                                                          While You Were Mine Historical-Fiction 4
                              World Without End (The Pillars of the Earth #2) Historical-Fiction 4
                                                            Wuthering Heights           Classics 6
```

                                                                        title        category_name
                                          1st to Die (Women's Murder Club #1)            Mystery 3
                                      A Flight of Arrows (The Pathfinders #2) Historical-Fiction 4
                                                             A Murder in Time            Mystery 3
                                                            A Paris Apartment Historical-Fiction 4
                            A Spy's Devotion (The Regency Spies of London #1) Historical-Fiction 4
                                      A Study in Scarlet (Sherlock Holmes #1)            Mystery 3
                                       A Time of Torment (Charlie Parker #14)            Mystery 3
                    Alice in Wonderland (Alice's Adventures in Wonderland #1)           Classics 6
                                                     And Then There Were None           Classics 6
                                                                  Animal Farm           Classics 6
                                                                      Beowulf           Classics 6
                                                       Between Shades of Gray Historical-Fiction 4
                                         Blood Defense (Samantha Brinkman #1)            Mystery 3
                                                Boar Island (Anna Pigeon #19)            Mystery 3
                                                                      Candide           Classics 6
                                          Career of Evil (Cormoran Strike #3)            Mystery 3
                             Delivering the Truth (Quaker Midwife Mystery #1)            Mystery 3
                                                                         Emma           Classics 6
                                           Extreme Prey (Lucas Davenport #26)            Mystery 3
    Forever and Forever: The Courtship of Henry Longfellow and Fanny Appleton Historical-Fiction 4
                                                    Girl With a Pearl Earring Historical-Fiction 4
                                                        Girl in the Blue Coat Historical-Fiction 4
                              Glory over Everything: Beyond The Kitchen House Historical-Fiction 4
                                                           Gone with the Wind           Classics 6
                                                   Hide Away (Eve Duncan #20)            Mystery 3
                                                         In a Dark, Dark Wood            Mystery 3
                                        In the Woods (Dublin Murder Squad #1)            Mystery 3
                                                                  Lilac Girls Historical-Fiction 4
                                               Little Women (Little Women #1)           Classics 6
                                                        Lost Among the Living Historical-Fiction 4
                                                         Love, Lies and Spies Historical-Fiction 4
                                                                  Most Wanted            Mystery 3
                                                                 Mrs. Houdini Historical-Fiction 4
                        Murder at the 42nd Street Library (Raymond Ambler #1)            Mystery 3
                                                              Of Mice and Men           Classics 6
                                                            Playing with Fire            Mystery 3
                                             Poisonous (Max Revere Novels #3)            Mystery 3
                                                        Sense and Sensibility           Classics 6
                                                                Sharp Objects            Mystery 3
                                                                     Starlark Historical-Fiction 4
                                         Tastes Like Fear (DI Marnie Rome #3)            Mystery 3
                                       That Darkness (Gardiner and Renner #1)            Mystery 3
     The Bachelor Girl's Guide to Murder (Herringford and Watts Mysteries #1)            Mystery 3
The Complete Stories and Poems (The Works of Edgar Allan Poe [Cameo Edition])           Classics 6
                                   The Constant Princess (The Tudor Court #1) Historical-Fiction 4
                                    The Cuckoo's Calling (Cormoran Strike #1)            Mystery 3
                                                                   The Exiled            Mystery 3
                                    The Girl In The Ice (DCI Erika Foster #1)            Mystery 3
                                                            The Girl You Lost            Mystery 3
                            The Guernsey Literary and Potato Peel Pie Society Historical-Fiction 4
                           The Hound of the Baskervilles (Sherlock Holmes #5)           Classics 6
                                                        The House by the Lake Historical-Fiction 4
                                                       The Invention of Wings Historical-Fiction 4
                                               The Last Mile (Amos Decker #2)            Mystery 3
                                             The Last Painting of Sara de Vos Historical-Fiction 4
                                                            The Little Prince           Classics 6
                                                    The Marriage of Opposites Historical-Fiction 4
                                                            The Metamorphosis           Classics 6
                              The Murder of Roger Ackroyd (Hercule Poirot #4)            Mystery 3
                          The Mysterious Affair at Styles (Hercule Poirot #1)            Mystery 3
       The No. 1 Ladies' Detective Agency (No. 1 Ladies' Detective Agency #1)            Mystery 3
                                                        The Passion of Dolssa Historical-Fiction 4
                                                          The Past Never Ends            Mystery 3
                                                   The Picture of Dorian Gray           Classics 6
                                                       The Pilgrim's Progress           Classics 6
                                                                 The Red Tent Historical-Fiction 4
                                                            The Secret Garden           Classics 6
                                                            The Secret Healer Historical-Fiction 4
                                            The Silkworm (Cormoran Strike #2)            Mystery 3
                                                    The Story of Hong Gildong           Classics 6
                                                                    The Widow            Mystery 3
                                                           Tipping the Velvet Historical-Fiction 4
                                                       Voyager (Outlander #3) Historical-Fiction 4
            What Happened on Beale Street (Secrets of the South Mysteries #2)            Mystery 3
                                                          While You Were Mine Historical-Fiction 4
                              World Without End (The Pillars of the Earth #2) Historical-Fiction 4
                                                            Wuthering Heights           Classics 6


## Query 6: JOIN example by highest-rated books per category

```sql
                                                                                                                                                                                                        title        category_name  rating price_inr
                                                                                                                                                                                            The Secret Garden           Classics 6       4      None
                                                                                                                                                                               Little Women (Little Women #1)           Classics 6       4      None
                                                                                                                                The Complete Stories and Poems (The Works of Edgar Allan Poe [Cameo Edition])           Classics 6       4      None
                                                                                                                                                                                    The Story of Hong Gildong           Classics 6       4      None
                                                                                                                                                                      A Flight of Arrows (The Pathfinders #2) Historical-Fiction 4       5      None
                                                                                                                                                                                                 Mrs. Houdini Historical-Fiction 4       5      None
                                                                                                                                                                                        The Passion of Dolssa Historical-Fiction 4       5      None
                                                                                                                                                                                       Voyager (Outlander #3) Historical-Fiction 4       5      None
                                                                                                                                                                                                 The Red Tent Historical-Fiction 4       5      None
                                                                                                                                                                                       Between Shades of Gray Historical-Fiction 4       5      None
                                                                                                                                                                                          While You Were Mine Historical-Fiction 4       5      None
                                                                                                                                                            A Spy's Devotion (The Regency Spies of London #1) Historical-Fiction 4       5      None
                                                                                                                                                                                    The Marriage of Opposites Historical-Fiction 4       4      None
                                                                                                                                                                                            A Paris Apartment Historical-Fiction 4       4      None
                                                                                                                                                              World Without End (The Pillars of the Earth #2) Historical-Fiction 4       4      None
                                                                                                                                                                                        Lost Among the Living Historical-Fiction 4       4      None
                                                                                                                                                                       A Time of Torment (Charlie Parker #14)            Mystery 3       5      None
                                                                                                                                            What Happened on Beale Street (Secrets of the South Mysteries #2)            Mystery 3       5      None
                                                                                                                                     The Bachelor Girl's Guide to Murder (Herringford and Watts Mysteries #1)            Mystery 3       5      None
                                                                                                                                                                            The Silkworm (Cormoran Strike #2)            Mystery 3       5      None
                                                                                                                                                                                            The Girl You Lost            Mystery 3       5      None
                                                                                                                                                                                                Sharp Objects            Mystery 3       4      None
                                                                                                                                                                                          The Past Never Ends            Mystery 3       4      None
                                                                                                                                                              The Murder of Roger Ackroyd (Hercule Poirot #4)            Mystery 3       4      None
                                                                                                                                                        Murder at the 42nd Street Library (Raymond Ambler #1)            Mystery 3       4      None
                                                                                                                                                             Delivering the Truth (Quaker Midwife Mystery #1)            Mystery 3       4      None
                                                                                                                                                          The Mysterious Affair at Styles (Hercule Poirot #1)            Mystery 3       4      None
                                                                                                                                       The No. 1 Ladies' Detective Agency (No. 1 Ladies' Detective Agency #1)            Mystery 3       4      None
                                                                                                                                                                                               Sophie's World         Philosophy 7       5      None
At The Existentialist CafÃ©: Freedom, Being, and apricot cocktails with: Jean-Paul Sartre, Simone de Beauvoir, Albert Camus, Martin Heidegger, Edmund Husserl, Karl Jaspers, Maurice Merleau-Ponty and others         Philosophy 7       5      None
                                                                                                                                                                 The Death of Humanity: and the Case for Life         Philosophy 7       4      None
                                                                                                                                                                                                 The Stranger         Philosophy 7       4      None
                                                                                                                                                                                   Chase Me (Paris Nights #2)            Romance 8       5      None
                                                                                                                                                                                                   Black Dust            Romance 8       5      None
                                                                                                                                                             A Gentleman's Position (Society of Gentlemen #3)            Romance 8       5      None
                                                                                                                                                                              Deep Under (Walker Security #1)            Romance 8       5      None
                                                                                                                                                                           First and First (Five Boroughs #3)            Romance 8       4      None
                                                                                                                                                                                     Something More Than This            Romance 8       4      None
                                                                                                                                                                                          Dirty (Dive Bar #1)            Romance 8       4      None
                                                                                                                                                                                            Imperfect Harmony            Romance 8       4      None
                                                                                                                                                                                Bounty (Colorado Mountain #7)            Romance 8       4      None
                                                                                                                                                      Scott Pilgrim's Precious Little Life (Scott Pilgrim #1)     Sequential-Art 5       5      None
                                                                                                                            Princess Jellyfish 2-in-1 Omnibus, Vol. 01 (Princess Jellyfish 2-in-1 Omnibus #1)     Sequential-Art 5       5      None
                                                                                                                                                                     Batman: The Dark Knight Returns (Batman)     Sequential-Art 5       5      None
                                                                                                                                                Superman Vol. 1: Before Truth (Superman by Gene Luen Yang #1)     Sequential-Art 5       5      None
                                                                                                                                                                                                     El Deafo     Sequential-Art 5       5      None
                                                                                                                                                                                                  Roller Girl     Sequential-Art 5       5      None
                                                                                                                                                                                              This One Summer     Sequential-Art 5       4      None
                                                                                                                                                                     The Nameless City (The Nameless City #1)     Sequential-Art 5       4      None
                                                                                                                                                       Outcast, Vol. 1: A Darkness Surrounds Him (Outcast #1)     Sequential-Art 5       4      None
                                                                                                                                                                                         Danganronpa Volume 1     Sequential-Art 5       4      None
                                                                                                                                                          Codename Baboushka, Volume 1: The Conclave of Death     Sequential-Art 5       4      None
                                                                                                                                                                                                Camp Midnight     Sequential-Art 5       4      None
                                                                                                                                                                 Fables, Vol. 1: Legends in Exile (Fables #1)     Sequential-Art 5       4      None
                                                                                                                                             Wonder Woman: Earth One, Volume One (Wonder Woman: Earth One #1)     Sequential-Art 5       4      None
                                                                                                                                                           So Cute It Hurts!!, Vol. 6 (So Cute It Hurts!! #6)     Sequential-Art 5       4      None
                                                                                                                                                                     Fruits Basket, Vol. 9 (Fruits Basket #9)     Sequential-Art 5       4      None
                                                                                                                                                                           1,000 Places to See Before You Die             Travel 2       5      None
                                                                                                                                           Full Moon over Noahâs Ark: An Odyssey to Mount Ararat and Beyond             Travel 2       4      None
                                                                                                                                                                             A Year in Provence (Provence #1)             Travel 2       4      None
                                                                                                                                                                                                   Some Women     Womens-Fiction 9       5      None
                                                                                                                                                                     Shopaholic Ties the Knot (Shopaholic #3)     Womens-Fiction 9       5      None
                                                                                                                                                                                 The Nanny Diaries (Nanny #1)     Womens-Fiction 9       5      None
                                                                                                                                                                       Something Borrowed (Darcy & Rachel #1)     Womens-Fiction 9       5      None
                                                                                                                                       I Had a Nice Time And Other Lies...: How to find love & sh*t like that     Womens-Fiction 9       4      None
                                                                                                                                                                                               Keep Me Posted     Womens-Fiction 9       4      None
                                                                                                                                                                                       Grey (Fifty Shades #4)     Womens-Fiction 9       4      None
                                                                                                                                                                                       The Undomestic Goddess     Womens-Fiction 9       4      None
                                                                                                                                                                        The Edge of Reason (Bridget Jones #2)     Womens-Fiction 9       4      None
```

                                                                                                                                                                                                        title        category_name  rating price_inr
                                                                                                                                                                                            The Secret Garden           Classics 6       4      None
                                                                                                                                                                               Little Women (Little Women #1)           Classics 6       4      None
                                                                                                                                The Complete Stories and Poems (The Works of Edgar Allan Poe [Cameo Edition])           Classics 6       4      None
                                                                                                                                                                                    The Story of Hong Gildong           Classics 6       4      None
                                                                                                                                                                      A Flight of Arrows (The Pathfinders #2) Historical-Fiction 4       5      None
                                                                                                                                                                                                 Mrs. Houdini Historical-Fiction 4       5      None
                                                                                                                                                                                        The Passion of Dolssa Historical-Fiction 4       5      None
                                                                                                                                                                                       Voyager (Outlander #3) Historical-Fiction 4       5      None
                                                                                                                                                                                                 The Red Tent Historical-Fiction 4       5      None
                                                                                                                                                                                       Between Shades of Gray Historical-Fiction 4       5      None
                                                                                                                                                                                          While You Were Mine Historical-Fiction 4       5      None
                                                                                                                                                            A Spy's Devotion (The Regency Spies of London #1) Historical-Fiction 4       5      None
                                                                                                                                                                                    The Marriage of Opposites Historical-Fiction 4       4      None
                                                                                                                                                                                            A Paris Apartment Historical-Fiction 4       4      None
                                                                                                                                                              World Without End (The Pillars of the Earth #2) Historical-Fiction 4       4      None
                                                                                                                                                                                        Lost Among the Living Historical-Fiction 4       4      None
                                                                                                                                                                       A Time of Torment (Charlie Parker #14)            Mystery 3       5      None
                                                                                                                                            What Happened on Beale Street (Secrets of the South Mysteries #2)            Mystery 3       5      None
                                                                                                                                     The Bachelor Girl's Guide to Murder (Herringford and Watts Mysteries #1)            Mystery 3       5      None
                                                                                                                                                                            The Silkworm (Cormoran Strike #2)            Mystery 3       5      None
                                                                                                                                                                                            The Girl You Lost            Mystery 3       5      None
                                                                                                                                                                                                Sharp Objects            Mystery 3       4      None
                                                                                                                                                                                          The Past Never Ends            Mystery 3       4      None
                                                                                                                                                              The Murder of Roger Ackroyd (Hercule Poirot #4)            Mystery 3       4      None
                                                                                                                                                        Murder at the 42nd Street Library (Raymond Ambler #1)            Mystery 3       4      None
                                                                                                                                                             Delivering the Truth (Quaker Midwife Mystery #1)            Mystery 3       4      None
                                                                                                                                                          The Mysterious Affair at Styles (Hercule Poirot #1)            Mystery 3       4      None
                                                                                                                                       The No. 1 Ladies' Detective Agency (No. 1 Ladies' Detective Agency #1)            Mystery 3       4      None
                                                                                                                                                                                               Sophie's World         Philosophy 7       5      None
At The Existentialist CafÃ©: Freedom, Being, and apricot cocktails with: Jean-Paul Sartre, Simone de Beauvoir, Albert Camus, Martin Heidegger, Edmund Husserl, Karl Jaspers, Maurice Merleau-Ponty and others         Philosophy 7       5      None
                                                                                                                                                                 The Death of Humanity: and the Case for Life         Philosophy 7       4      None
                                                                                                                                                                                                 The Stranger         Philosophy 7       4      None
                                                                                                                                                                                   Chase Me (Paris Nights #2)            Romance 8       5      None
                                                                                                                                                                                                   Black Dust            Romance 8       5      None
                                                                                                                                                             A Gentleman's Position (Society of Gentlemen #3)            Romance 8       5      None
                                                                                                                                                                              Deep Under (Walker Security #1)            Romance 8       5      None
                                                                                                                                                                           First and First (Five Boroughs #3)            Romance 8       4      None
                                                                                                                                                                                     Something More Than This            Romance 8       4      None
                                                                                                                                                                                          Dirty (Dive Bar #1)            Romance 8       4      None
                                                                                                                                                                                            Imperfect Harmony            Romance 8       4      None
                                                                                                                                                                                Bounty (Colorado Mountain #7)            Romance 8       4      None
                                                                                                                                                      Scott Pilgrim's Precious Little Life (Scott Pilgrim #1)     Sequential-Art 5       5      None
                                                                                                                            Princess Jellyfish 2-in-1 Omnibus, Vol. 01 (Princess Jellyfish 2-in-1 Omnibus #1)     Sequential-Art 5       5      None
                                                                                                                                                                     Batman: The Dark Knight Returns (Batman)     Sequential-Art 5       5      None
                                                                                                                                                Superman Vol. 1: Before Truth (Superman by Gene Luen Yang #1)     Sequential-Art 5       5      None
                                                                                                                                                                                                     El Deafo     Sequential-Art 5       5      None
                                                                                                                                                                                                  Roller Girl     Sequential-Art 5       5      None
                                                                                                                                                                                              This One Summer     Sequential-Art 5       4      None
                                                                                                                                                                     The Nameless City (The Nameless City #1)     Sequential-Art 5       4      None
                                                                                                                                                       Outcast, Vol. 1: A Darkness Surrounds Him (Outcast #1)     Sequential-Art 5       4      None
                                                                                                                                                                                         Danganronpa Volume 1     Sequential-Art 5       4      None
                                                                                                                                                          Codename Baboushka, Volume 1: The Conclave of Death     Sequential-Art 5       4      None
                                                                                                                                                                                                Camp Midnight     Sequential-Art 5       4      None
                                                                                                                                                                 Fables, Vol. 1: Legends in Exile (Fables #1)     Sequential-Art 5       4      None
                                                                                                                                             Wonder Woman: Earth One, Volume One (Wonder Woman: Earth One #1)     Sequential-Art 5       4      None
                                                                                                                                                           So Cute It Hurts!!, Vol. 6 (So Cute It Hurts!! #6)     Sequential-Art 5       4      None
                                                                                                                                                                     Fruits Basket, Vol. 9 (Fruits Basket #9)     Sequential-Art 5       4      None
                                                                                                                                                                           1,000 Places to See Before You Die             Travel 2       5      None
                                                                                                                                           Full Moon over Noahâs Ark: An Odyssey to Mount Ararat and Beyond             Travel 2       4      None
                                                                                                                                                                             A Year in Provence (Provence #1)             Travel 2       4      None
                                                                                                                                                                                                   Some Women     Womens-Fiction 9       5      None
                                                                                                                                                                     Shopaholic Ties the Knot (Shopaholic #3)     Womens-Fiction 9       5      None
                                                                                                                                                                                 The Nanny Diaries (Nanny #1)     Womens-Fiction 9       5      None
                                                                                                                                                                       Something Borrowed (Darcy & Rachel #1)     Womens-Fiction 9       5      None
                                                                                                                                       I Had a Nice Time And Other Lies...: How to find love & sh*t like that     Womens-Fiction 9       4      None
                                                                                                                                                                                               Keep Me Posted     Womens-Fiction 9       4      None
                                                                                                                                                                                       Grey (Fifty Shades #4)     Womens-Fiction 9       4      None
                                                                                                                                                                                       The Undomestic Goddess     Womens-Fiction 9       4      None
                                                                                                                                                                        The Edge of Reason (Bridget Jones #2)     Womens-Fiction 9       4      None
