from collections import namedtuple
from typing import Union, Optional

from pybliometrics.superclasses import Retrieval
from pybliometrics.utils import make_int_if_possible, chained_get


class PublicationLookup(Retrieval):

    @property
    def id(self) -> Optional[int]:
        """ID of the document (same as EID without "2-s2.0-")."""
        return make_int_if_possible(chained_get(self._json, ['publication', 'id']))

    @property
    def title(self) -> Optional[str]:
        """Publication title"""
        return chained_get(self._json, ['publication', 'title'])

    @property
    def doi(self) -> Optional[str]:
        """Digital Object Identifier (DOI)"""
        return chained_get(self._json, ['publication', 'doi'])

    @property
    def type(self) -> Optional[str]:
        """Type of publication"""
        return chained_get(self._json, ['publication', 'type'])

    @property
    def publication_year(self) -> Optional[int]:
        """Year of publication"""
        return make_int_if_possible(chained_get(self._json, ['publication', 'publicationYear']))

    @property
    def citation_count(self) -> Optional[int]:
        """Count of citations"""
        return make_int_if_possible(chained_get(self._json, ['publication', 'citationCount']))

    @property
    def source_title(self) -> Optional[str]:
        """Title of source"""
        return chained_get(self._json, ['publication', 'sourceTitle'])

    @property
    def topic_id(self) -> Optional[int]:
        """Topic id"""
        return make_int_if_possible(chained_get(self._json, ['publication', 'topicId']))

    @property
    def topic_cluster_id(self) -> Optional[int]:
        """Topic cluster id"""
        return make_int_if_possible(chained_get(self._json, ['publication', 'topicClusterId']))

    @property
    def link(self) -> Optional[str]:
        """URL link"""
        return chained_get(self._json, ['link', '@href'])

    @property
    def authors(self) -> Optional[list[namedtuple]]:
        out = []
        fields = 'id name link'
        auth = namedtuple('Author', fields)
        for item in chained_get(self._json, ['publication', 'authors'], []):
            new = auth(id=make_int_if_possible(item['id']), name=item.get('name'),
                       link=chained_get(item, ['link', '@href']))
            out.append(new)
        return out or None

    @property
    def institutions(self) -> Optional[list[namedtuple]]:
        out = []
        fields = 'id name country country_code link'
        auth = namedtuple('Institution', fields)
        for item in chained_get(self._json, ['publication', 'institutions'], []):
            new = auth(id=make_int_if_possible(item['id']), name=item.get('name'),
                       country=item.get('country'), country_code=item.get('countryCode'),
                       link=chained_get(item, ['link', '@href']))
            out.append(new)
        return out or None

    @property
    def sdgs(self) -> Optional[list[str]]:
        """Sustainable Development Goals."""
        return chained_get(self._json, ['publication', 'sdg'])

    def __init__(self,
                 identifier: int = None,
                 refresh: Union[bool, int] = False,
                 **kwds: str
                 ) -> None:
        """Interaction with the Publication Lookup API.
                """
        self._view = ''
        self._refresh = refresh
        Retrieval.__init__(self, identifier=str(identifier), **kwds)
