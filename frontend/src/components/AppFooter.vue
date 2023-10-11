<template>
  <div>
    <footer class="site-footer">
      <div class="container-liquid">
        <div class="row">
          <div class="col-10">
            <div class="row">
              <div class="col-12 col-sm-8 col-md-4">
                <div
                  id="os-theme-contact-address"
                  class="contact-address"
                >
                  <p>
                    LA STRUCTURE<br />
                    ADRESSE<br />
                  </p>
                </div>
              </div>
              <div
                class="col-12 col-sm-4 col-md-4 d-flex justify-content-md-center"
              >
                <nav
                  role="navigation"
                >
                  <h2
                    class="visually-hidden"
                  >
                    Menu footer
                  </h2>

                  <ul class="list-unstyled">
                    <li>
                      <a href="/"> {{ title }} </a>
                    </li>
                    <li>
                      <router-link to="/contact">
                        Contact
                      </router-link>
                    </li>
                    <li>
                      <router-link to="/credits">
                        Credits
                      </router-link>
                    </li>
                    <li>
                      <router-link to="/legalnotice">
                        Mentions légales
                      </router-link>
                    </li>
                    <li>
                      <router-link to="/datapolicy">
                        Données personnelles
                      </router-link>
                    </li>
                  </ul>
                </nav>
              </div>
            </div>
          </div>
          <div class="col-2">
            <a href="#" @click.prevent="backToTop()" class="back-to-top" title="Back to top">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                viewBox="0 0 16 16"
                fill="var(--link-color-bg-secondary)"
              >
                <path
                  d="m0 8 1.455 1.455 5.506-5.506V16h2.078V3.948l5.506 5.507L16 8 8 0Z"
                ></path>
              </svg>
            </a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>
<script setup>
const title = import.meta.env.VITE_APP_TITLE;
</script>
