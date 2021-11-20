## Jednoduse posilejte informace o aktualni koronavirove situaci (od Ministerstva Zdravotnictvi (mzcr.cz)) primo na vas discord
## github.com/exzedik
## ---------------------
## vyhledavaci klice od mzcr:
## provedene_testy_celkem
## potvrzene_pripady_celkem
## aktivni_pripady
## vyleceni
## umrti
## aktualne_hospitalizovani
## provedene_testy_vcerejsi_den
## potvrzene_pripady_vcerejsi_den
## provedene_testy_vcerejsi_den_datum
## potvrzene_pripady_vcerejsi_den_datum
## provedene_antigenni_testy_celkem
## provedene_antigenni_testy_vcerejsi_den
## provedene_antigenni_testy_vcerejsi_den_datum
## vykazana_ockovani_celkem
## vykazana_ockovani_vcerejsi_den
## vykazana_ockovani_vcerejsi_den_datum
## potvrzene_pripady_65_celkem
## potvrzene_pripady_65_vcerejsi_den
## potvrzene_pripady_65_vcerejsi_den_datum
## ockovane_osoby_celkem
## ockovane_osoby_vcerejsi_den
## ockovane_osoby_vcerejsi_den_datum
import requests, json, pycron, time

webhook = 'SEM VLOZTE VAS DISCORD WEBHOOK'

def covidinfo(request):
    response = requests.get('https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/zakladni-prehled.json')
    covid = json.loads(response.text)
    try:
        for info in covid['data']:
            return(info[request])
    except KeyError:
        return('[KeyError] Hledany klic nenalezen.')

def job():
    data = {
        "content": "",
        "username": "COVID-19 Info",
        "avatar_url": "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/285/microbe_1f9a0.png",
        "embeds": [{
                "title": "Aktuální informace ohledně nákazy COVID-19 :flag_cz::microbe:",
                "description": f"Informace čerpány z mzcr.cz\n\nCelkem provedeno **{covidinfo('provedene_testy_celkem')}** testů,\n   z toho **{covidinfo('potvrzene_pripady_celkem')}** pozitivních (**{covidinfo('potvrzene_pripady_vcerejsi_den')}** včera).\n\n**{covidinfo('aktivni_pripady')}** Aktivních případů\n**{covidinfo('vyleceni')}** Vyléčených\n**{covidinfo('umrti')}** Úmrtí *({int(covidinfo('umrti'))/int(covidinfo('potvrzene_pripady_celkem')):.4f}%)*\n**{covidinfo('aktualne_hospitalizovani')}** Hospitalizovaných\n**{covidinfo('ockovane_osoby_celkem')}** Očkovaných (**{covidinfo('ockovane_osoby_vcerejsi_den')}** včera) :syringe:",
                "color": "3066993",
        }]
    }
    headers = {
        "Content-Type": "application/json"
    }
    result = requests.post(webhook, json=data, headers=headers)
    if 200 <= result.status_code < 300:
        print(f"Webhook sent {result.status_code}")
    else:
        print(f"Not sent with {result.status_code}, response:\n{result.json()}")
while True:
    if pycron.is_now('0 6 * * mon-sun'):
        job()
    time.sleep(60)