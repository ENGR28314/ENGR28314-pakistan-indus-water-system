from pathlib import Path
import pandas as pd

BASE = Path(__file__).parent

PROVINCES = [
    'Gilgit-Baltistan', 'Khyber Pakhtunkhwa (KPK)', 'Punjab', 'Sindh',
    'Balochistan', 'Azad Jammu & Kashmir (AJK)', 'Islamabad Capital Territory (ICT)'
]

ROWS = [
# rivers
('River','Indus','Indus Basin','Gilgit-Baltistan; Khyber Pakhtunkhwa; Punjab; Sindh','Main river','Upper Indus system','Arabian Sea / Indus Delta','Kabul; Panjnad; major northern tributaries','Main trunk of Pakistan Indus Basin'),
('River','Gilgit','Indus Basin','Gilgit-Baltistan','Tributary','Upper Gilgit-Baltistan','Indus near Bunji','Indus','Upper Indus tributary'),
('River','Shyok','Indus Basin','Gilgit-Baltistan','Tributary','Upper Shyok basin','Indus','Indus','Upper Indus tributary'),
('River','Shigar','Indus Basin','Gilgit-Baltistan','Tributary','Shigar valley','Indus near Skardu','Indus','Upper Indus tributary'),
('River','Kabul','Indus Basin','Khyber Pakhtunkhwa (KPK)','Tributary','Kabul basin','Indus near Attock','Indus','Major western tributary'),
('River','Swat','Indus Basin','Khyber Pakhtunkhwa (KPK)','Tributary','Upper Swat','Kabul near Charsadda','Kabul','Important KP river'),
('River','Kurram','Indus Basin','Khyber Pakhtunkhwa (KPK)','Tributary','Kurram basin','Indus system','Indus system','Western tributary'),
('River','Gomal','Indus Basin','Khyber Pakhtunkhwa (KPK); Balochistan','Tributary','Gomal basin','Indus near D.I. Khan','Indus','Cross-regional western tributary'),
('River','Jhelum','Indus Basin','Azad Jammu & Kashmir (AJK); Punjab','Main tributary','Kashmir/Jhelum headwaters','Chenab system near Trimmu','Chenab','Regulated by Mangla and Rasul system'),
('River','Neelum','Indus Basin','Azad Jammu & Kashmir (AJK)','Tributary','Upper Neelum Valley','Jhelum at Muzaffarabad','Jhelum','Important AJ&K tributary'),
('River','Poonch','Indus Basin','Azad Jammu & Kashmir (AJK); Punjab','Tributary','Poonch basin','Jhelum system','Jhelum','Transboundary basin tributary'),
('River','Chenab','Indus Basin','Punjab','Main tributary','Upper Chenab','Panjnad','Jhelum; Panjnad','Central Punjab river'),
('River','Ravi','Indus Basin','Punjab','Main tributary','Upper Ravi','Chenab/Panjnad system','Chenab/Panjnad','Bari Doab system'),
('River','Sutlej','Indus Basin','Punjab','Main tributary','Upper Sutlej','Panjnad','Panjnad','Eastern river in wider Indus system'),
('River','Panjnad','Indus Basin','Punjab','Combined river','Jhelum/Chenab/Ravi/Sutlej system','Indus near Mithankot','Indus','Carries combined Punjab-river flows'),
('River','Hub','Coastal basin','Balochistan; Sindh','River','Hub basin','Arabian Sea','Coastal drainage','Important local water-supply basin'),
('River','Soan','Indus Basin','Islamabad Capital Territory (ICT); Punjab','Tributary','Potohar / Islamabad region','Indus via the lower Indus system','Indus system','Important river of the Islamabad-Potohar region'),
('River','Korang','Indus Basin','Islamabad Capital Territory (ICT); Punjab','Tributary','Margalla/Islamabad region','Soan River','Soan','Local tributary of the Soan system'),
('River','Haro','Indus Basin','Islamabad Capital Territory (ICT); Khyber Pakhtunkhwa (KPK); Punjab','Tributary','Haro basin','Indus near Attock','Indus','Cross-regional tributary'),
('River','Hingol','Balochistan coastal basin','Balochistan','River','Balochistan uplands','Arabian Sea','Coastal drainage','Major coastal river'),
('River','Dasht','Balochistan coastal basin','Balochistan','River','Central Balochistan','Arabian Sea/coastal basin','Coastal drainage','Major Balochistan river'),
('River','Mula','Local basin','Balochistan','River','Jhal Magsi region','Lower Mula basin','Local drainage','Associated with Naulong project'),
('River','Gaj','Sindh local basin','Sindh','River','Kirthar Range','Lower Sindh','Local drainage','Associated with Nai Gaj Dam'),
# dams
('Dam','Tarbela Dam','Indus','Khyber Pakhtunkhwa (KPK)','Operational','Indus upstream','Indus downstream','', 'Major storage/hydropower dam'),
('Dam','Diamer Basha Dam','Indus','Gilgit-Baltistan; Khyber Pakhtunkhwa (KPK)','Under construction','Upper Indus near Diamer','Indus toward Tarbela','','Major storage project'),
('Dam','Dasu Hydropower Project','Indus','Khyber Pakhtunkhwa (KPK)','Under construction / staged','Upper Indus','Indus downstream','','Major hydropower project'),
('Dam','Mohmand Dam','Swat','Khyber Pakhtunkhwa (KPK)','Under construction','Swat River upstream of Munda','Swat downstream','','WAPDA identifies site about 5 km upstream of Munda Head Works'),
('Dam','Warsak Dam','Kabul','Khyber Pakhtunkhwa (KPK)','Operational','Kabul upstream','Kabul downstream','','Hydropower and irrigation regulation'),
('Dam','Mangla Dam','Jhelum','Azad Jammu & Kashmir (AJK)','Operational','Jhelum upstream','Jhelum downstream toward Rasul','','Major storage/hydropower dam'),
('Dam','Kurram Tangi Dam Project','Kurram','Khyber Pakhtunkhwa (KPK)','Project','Kurram upstream','Kurram downstream','','Water storage/irrigation project'),
('Dam','Nai Gaj Dam','Gaj','Sindh','Project','Gaj River','Gaj downstream','','Water storage/irrigation project'),
('Dam','Naulong Storage Dam','Mula','Balochistan','Project','Mula River','Mula downstream','','Water storage project'),
# barrages
('Barrage','Nowshera Head Works','Kabul','Khyber Pakhtunkhwa (KPK)','Operational/reference','Kabul upstream','Kabul downstream','','Kabul control location'),
('Barrage','Chashma Barrage','Indus','Punjab; Khyber Pakhtunkhwa (KPK) command','Operational','Indus upstream','Indus downstream','','Feeds Chashma-Jhelum Link'),
('Barrage','Jinnah Barrage','Indus','Punjab','Operational','Indus upstream','Indus downstream','','Indus control structure'),
('Barrage','Rasul Barrage','Jhelum','Punjab','Operational','Jhelum upstream','Jhelum downstream','','Major Jhelum diversion structure'),
('Barrage','Marala Barrage / Headworks','Chenab','Punjab','Operational','Chenab upstream','Chenab downstream','','Associated with Marala-Ravi Link'),
('Barrage','Khanki Barrage','Chenab','Punjab','Operational','Chenab upstream','Chenab downstream','','Major Chenab diversion structure'),
('Barrage','Qadirabad Barrage','Chenab','Punjab','Operational','Chenab upstream','Chenab downstream','','Receives Rasul-Qadirabad Link'),
('Barrage','Trimmu Barrage','Chenab','Punjab','Operational','Chenab/Jhelum system','Chenab downstream','','Major lower Chenab control point'),
('Barrage','Balloki Barrage / Headworks','Ravi','Punjab','Operational','Ravi upstream','Ravi downstream','','Major Ravi control structure'),
('Barrage','Sidhnai Barrage','Ravi','Punjab','Operational','Ravi upstream','Ravi downstream','','Associated with Trimmu-Sidhnai system'),
('Barrage','Sulemanki Barrage','Sutlej','Punjab','Operational','Sutlej upstream','Sutlej downstream','','Major Sutlej control structure'),
('Barrage','Islam Barrage','Sutlej','Punjab','Operational','Sutlej upstream','Sutlej downstream','','Sutlej irrigation system'),
('Barrage','Panjnad Barrage','Panjnad','Punjab','Operational','Punjab rivers upstream','Indus via Panjnad','','Major combined-flow control point'),
('Barrage','Taunsa Barrage','Indus','Punjab','Operational','Indus upstream','Indus downstream','','Major Indus diversion structure'),
('Barrage','Guddu Barrage','Indus','Sindh','Operational','Indus upstream','Indus downstream','','Major Sindh diversion structure'),
('Barrage','Sukkur Barrage','Indus','Sindh','Operational','Indus upstream','Indus downstream','','Major Sindh irrigation structure'),
('Barrage','Kotri Barrage','Indus','Sindh','Operational','Indus upstream','Indus Delta / Arabian Sea','','Lowest major barrage in Indus irrigation system'),
# link canals
('Link Canal','Chashma-Jhelum Link','Indus → Jhelum','Punjab; Khyber Pakhtunkhwa (KPK) command','Operational','Chashma Barrage','Jhelum/Rasul system','','Major inter-river link'),
('Link Canal','Rasul-Qadirabad Link','Jhelum → Chenab','Punjab','Operational','Rasul Barrage','Qadirabad Barrage','','Jhelum-Chenab link'),
('Link Canal','Marala-Ravi Link','Chenab → Ravi','Punjab','Operational','Marala Headworks','Ravi system','','Chenab-Ravi link'),
('Link Canal','Qadirabad-Balloki Link','Chenab → Ravi','Punjab','Operational','Qadirabad Barrage','Balloki Headworks','','Chenab-Ravi link'),
('Link Canal','Balloki-Sulemanki Link','Ravi → Sutlej','Punjab','Operational','Balloki Headworks','Sulemanki Barrage','','Ravi-Sutlej link'),
('Link Canal','Trimmu-Sidhnai Link','Chenab → Ravi','Punjab','Operational','Trimmu Barrage','Sidhnai Barrage','','Major inter-river link'),
('Link Canal','Sidhnai-Mailsi-Bahawalpur Link','Ravi → Sutlej system','Punjab','Operational','Sidhnai system','Sutlej command','','Major Punjab link corridor'),
('Link Canal','Taunsa-Panjnad Link','Indus → Panjnad','Punjab','Operational','Taunsa Barrage','Panjnad Barrage','','Indus-to-Punjab-rivers link'),
# confluences
('Confluence','Indus + Kabul','Indus / Kabul','Khyber Pakhtunkhwa (KPK)','Confluence','Kabul approaches Attock','Indus downstream','Kabul joins Indus','Major western confluence'),
('Confluence','Neelum + Jhelum','Neelum / Jhelum','Azad Jammu & Kashmir (AJK)','Confluence','Neelum approaches Muzaffarabad','Jhelum downstream','Neelum joins Jhelum','Important AJK confluence'),
('Confluence','Swat + Kabul','Swat / Kabul','Khyber Pakhtunkhwa (KPK)','Confluence','Swat approaches Charsadda','Kabul downstream','Swat joins Kabul','Important KP confluence'),
('Confluence','Jhelum + Chenab','Jhelum / Chenab','Punjab','Confluence','Jhelum/Chenab system','Combined flow toward Panjnad','Jhelum joins Chenab','Lower Punjab river system'),
('Confluence','Ravi + Chenab system','Ravi / Chenab','Punjab','Confluence','Lower Ravi','Panjnad system','Ravi contributes to combined system','Panjnad-system relationship'),
('Confluence','Sutlej + Chenab','Sutlej / Chenab','Punjab','Confluence','Sutlej approaches Panjnad','Panjnad','Sutlej joins combined Punjab rivers','Panjnad formation'),
('Confluence','Panjnad + Indus','Panjnad / Indus','Punjab','Confluence','Panjnad approaches Mithankot','Lower Indus','Panjnad joins Indus','Major transition into lower Indus'),
]

COLS = ['asset_type','name','river_system','province_region','status','upstream','downstream','confluences','notes']

def load_data():
    df = pd.DataFrame(ROWS, columns=COLS)
    return {'assets': df}
