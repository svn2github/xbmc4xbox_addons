#!/usr/bin/env python
# -*- coding: utf-8 -*-
BASE=[
('http://supertv.3owl.com/USA.xml','United States'),
('http://supertv.3owl.com/United%20Kingdom.xml', 'United Kingdom'),
('http://supertv.3owl.com/Deutschland.xml','Deutschland'),
('http://supertv.3owl.com/Ellada.xml', 'Ελλάδα'),
('http://supertv.3owl.com/Espana.xml', 'España'),
('http://supertv.3owl.com/France.xml', 'France'),
('http://supertv.3owl.com/India.xml', 'India'),
('http://supertv.3owl.com/Italia.xml', 'Italia'),
('http://supertv.3owl.com/Magyarorszag.xml','Magyarország'),
('http://supertv.3owl.com/Oesterreich.xml','Österreich'),
('http://supertv.3owl.com/Portugal.xml', 'Portugal'),
('http://supertv.3owl.com/Rossija.xml', 'Россия'),
('http://supertv.3owl.com/Svizzera%20Schweiz%20Suisse.xml','Svizzera/Schweiz/Suisse'),
('http://supertv.3owl.com/Turkiye.xml','Türkiye'),
('http://supertv.3owl.com/Viet%20Nam.xml','Việt Nam'),
#('http://supertv.3owl.com/list.xml',"rtmpGUI list"),
('http://apps.ohlulz.com/rtmpgui/list.xml',"rtmpGUI list"),
('http://home.no/chj191/LiveTV.xml',"blackoutworm's list"),
#('http://home.no/chj191/xxx.xml',"blackoutworm's XXX list"),
]
if __name__ == "__main__": from resources.lib.main import main;main(BASE)