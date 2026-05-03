# Atlas Radio Club — Flipbook

A static reimagining of [atlasradio.club](https://atlasradio.club) as a page-flipping book, with a companion world map that pins each show to the city it came from.

## What's here

- `index.html` — single page; shell for the flipbook + map views
- `styles.css` — type, palette, and the CSS 3D flipbook
- `app.js` — flipbook logic, view toggle, and Leaflet map setup
- `data.js` — the show roster: title, host, city, country, lat/lng, SoundCloud URL

## Run it

It's static. Open `index.html` in a browser, or serve the folder:

```sh
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Add or edit a show

Open `data.js` and append an object to `SHOWS`:

```js
{
  title: "Show name",
  host: "host handle",
  city: "City",
  country: "Country",
  lat: 0.0,
  lng: 0.0,
  description: "One-line blurb that shows on the page.",
  soundcloudUrl: "https://soundcloud.com/atlasradioclub/your-track-slug"
}
```

The flipbook page and the map pin are both generated from this list. `soundcloudUrl` can be any track URL on the `@atlasradioclub` profile — the SoundCloud embed widget handles the rest.

## Controls

- **Click the right side of the page** or hit **→** to flip forward
- **Click the left side** or **←** to flip back
- Toggle between **Flipbook** and **World Map** in the top bar
- On the map, click a pin then **open page →** to jump to that show in the flipbook

## Stack

No build step. Vanilla HTML/CSS/JS. Leaflet + Carto dark tiles for the map. Google Fonts (Cormorant Garamond + Space Mono).
