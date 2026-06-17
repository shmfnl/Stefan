# Backend styling – phase 11c visible secondary fields

Deze build corrigeert de vorige phase 11c-build:
- de secondary button velden bestonden technisch al
- maar stonden per ongeluk niet in de Settings-view

## Nu zichtbaar in Settings
- Secondary knop achtergrond
- Secondary knop tekst
- Secondary knop hover

## Veiligheid
- settings-structuur blijft op de stabiele compat-lijn
- secondary waarden lopen via `config_parameter`
- géén extra kolommen op `res.company`
- navbar/MuK CSS blijft behouden
