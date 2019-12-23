from genknogra.entitylinking import processwiki


def test_no_links():
    sentence = "sentence with no links."
    stripped_sentence, link_page, description, span_start, span_end = processwiki.get_wikilinks(
        sentence
    )

    assert stripped_sentence == "sentence with no links."
    assert link_page == []
    assert span_start == []
    assert span_end == []


def test_onelink_no_description():
    sentence = "sentence [[with]] one link with no description."
    stripped_sentence, link_page, description, span_start, span_end = processwiki.get_wikilinks(
        sentence
    )

    assert stripped_sentence == "sentence with one link with no description."
    assert link_page == ["with"]
    assert span_start == [9]
    assert span_end == [13]


def test_onelink_with_description():
    sentence = "sentence [[linking_page|with]] one link with description."
    stripped_sentence, link_page, description, span_start, span_end = processwiki.get_wikilinks(
        sentence
    )

    assert stripped_sentence == "sentence with one link with description."
    assert link_page == ["linking_page"]
    assert span_start == [9]
    assert span_end == [13]


def test_multilink_no_description():
    sentence = "sentence [[with]] multiple link with [[no]] description."
    stripped_sentence, link_page, description, span_start, span_end = processwiki.get_wikilinks(
        sentence
    )

    assert stripped_sentence == "sentence with multiple link with no description."
    assert link_page == ["with", "no"]
    assert span_start == [9, 33]
    assert span_end == [13, 35]


def test_multilink_with_description():
    sentence = "sentence [[linking_page|with]] multiple link with [[linking_page|no]] description."
    stripped_sentence, link_page, description, span_start, span_end = processwiki.get_wikilinks(
        sentence
    )

    assert stripped_sentence == "sentence with multiple link with no description."
    assert link_page == ["linking_page", "linking_page"]
    assert span_start == [9, 33]
    assert span_end == [13, 35]
