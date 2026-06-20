# ELEMENTS — Luxury Lifestyle Ecommerce (Cloud Computing Assignment)

Modern minimal luxury ecommerce storefront, deployed on Google Cloud
Platform with a serverless order backend and GitHub Actions CI/CD.

## Project structure
```
elements/
├── index.html              # Homepage (hero, products, order form, contact)
├── style.css                # Site styling
├── script.js                 # Product rendering + order form submit logic
├── products.json             # Product catalog
├── assets/                   # Product images
├── pages/                    # about.html, contact.html, products.html
├── backend/
│   ├── order_handler.py      # Cloud Function: receives order form submissions
│   └── requirements.txt
└── .github/workflows/
    └── deploy.yml             # CI/CD: validates + deploys to GCS on push to main
```

## Before you deploy
1. Deploy `backend/order_handler.py` as a Cloud Function (`handle-order-v3`,
   HTTP trigger, unauthenticated, Python 3.11, region `asia-south1`).
2. `ORDER_FUNCTION_URL` in `script.js` is already set to
   `https://handle-order-v3-927825491730.asia-south1.run.app` --
   update it only if you redeploy the function under a different name/URL.
3. Create a GCS bucket (e.g. `elements-ecommerce-sneha`), enable static
   website hosting (main page `index.html`), make it public
   (`allUsers` -> Storage Object Viewer).
4. Update the bucket name inside `.github/workflows/deploy.yml` if you
   used a different bucket name.
5. Add your service account JSON key to GitHub repo secrets as
   `GCP_SA_KEY` (Settings -> Secrets and variables -> Actions).
6. Push to `main` -- GitHub Actions will validate and deploy automatically.

## Live site
`https://storage.googleapis.com/[YOUR-BUCKET-NAME]/index.html`
