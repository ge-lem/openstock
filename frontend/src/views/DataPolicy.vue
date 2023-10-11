<template>
  <div class="container text-justify p-4 col-lg-8 offset-lg-2">
    <main class="row">
      <h1 class="os-page-title">Crédits</h1>
      <PartageTools />

      <div class="os-page-content">
        <h3>Politique de confidentialité</h3>
        <p>
          LA STRUCTURE, dont le siège social est situé ADRESSE, en sa qualité de responsable du
          traitement, s'engage à ce que les traitements de données personnelles
          effectués sur les sites internet et intranet qu’elle héberge, soient
          conformes au règlement général sur la protection des données (RGPD) et
          à la loi Informatique et Libertés.
        </p>
        <ol>
          <li>Les données que nous collectons</li>
          <li>Comment utilisons-nous les données que nous collectons ?</li>
          <li>Qui sont les destinataires des données que nous collectons ?</li>
          <li>Combien de temps conservons-nous vos données ?</li>
          <li>Comment vos données sont-elles protégées ?</li>
          <li>Quels sont vos droits sur vos données ?</li>
        </ol>
        <h3>1. Les données que nous collectons</h3>
        <p>
          En utilisant les sites internet et intranet de LA STRUCTURE, vous êtes amenés à nous transmettre des informations, dont
          certaines sont de nature à vous identifier :
        </p>
        <h4>Données des formulaires</h4>
        <p>
          Nous collectons les informations strictement nécessaires pour répondre
          à votre demande.
        </p>
        <h4>Les cookies</h4>
        <p>
          Nous utilisons différents cookies pour mesurer l’audience et intégrer
          des services permettant d’améliorer l’interactivité du site.
        </p>
        <p>
          <strong>Les cookies essentiels</strong> : ces cookies sont
          indispensables pour assurer le bon fonctionnement du site.
        </p>
        <h3>2. Comment utilisons-nous les données que nous collectons ?</h3>
        <p>Nous utilisons les données que nous recueillons afin de :</p>
        <ul>
          <li>
            répondre à vos demandes sur la base légale de l’intérêt légitime.
          </li>
          <li>
            conserver vos données de connexion pour répondre à une obligation
            légale
          </li>
        </ul>
        <h3>3. Qui sont les destinataires des données que nous collectons ?</h3>
        <ul>
          <li>
            <p>
              les destinataires de vos données sont les services communication
              et informatique ainsi que les personnels autorisés de LA STRUCTURE.
            </p>
          </li>
          <li>
            conformément à la réglementation en vigueur, les données peuvent
            être transmises aux autorités compétentes sur requête dans le cas de
            la recherche des auteurs d’infractions commises sur internet.
          </li>
          <li>
            vos données peuvent être collectées par des tiers (réseaux sociaux
            et plateformes de vidéos) pour des finalités qui leur sont propres,
            conformément à leur politique de confidentialité. LA STRUCTURE n’a 
            pas le contrôle sur ces cookies tiers.
          </li>
        </ul>
        <h3>4. Combien de temps conservons-nous vos données ?</h3>
        <p>
          Vos données sont conservées pendant la durée nécessaire à la
          réalisation des finalités poursuivies telles qu’énoncées dans la
          présente politique, et ce, conformément à la législation applicable :
        </p>
        <ul>
          <li>
            les données utilisées aux fins de réponse à vos demandes à partir
            des formulaires sont conservées le temps nécessaire au traitement de
            votre demande et pour une durée maximale d’un an.
          </li>
          <li>
            les données de connexion et navigation sont conservées légalement 36
            mois.
          </li>
        </ul>
        <h3>5. Comment vos données sont-elles protégées ?</h3>
        <p>
          Nous prenons des mesures adéquates sur le plan de la technique et de
          l’organisation pour interdire l’accès non autorisé ou la modification,
          divulgation, perte ou destruction de vos données. A cet effet, le
          sites bénéficient d’une connexion
          sécurisée de type « SSL » qui crypte et protège les données lors de
          leur transmission sur le réseau internet. Aussi, l’accès à vos données
          personnelles et à leur traitement est limité aux seules personnes
          autorisées.
        </p>
        <h3>6. Quels sont vos droits sur vos données ?</h3>
        <p>
          Conformément aux lois et règlements applicables en matière de
          protection des données personnelles, vous bénéficiez d’un certain
          nombre de droits relatifs à vos données en fonction de la base légale
          du traitement auxquelles elles se rapportent, à savoir :
        </p>
        <ul>
          <li>un droit d’accès</li>
          <li>un droit de rectification</li>
          <li>un droit à l’effacement ou droit à l’oubli</li>
          <li>un droit à la limitation du traitement</li>
          <li>un droit d’opposition au traitement</li>
          <li>
            le droit de retirer votre consentement à tout moment Pour exercer
            ces droits, vous pouvez contacter notre Délégué à la protection des
            données personnelles à l’adresse suivante :
            <a href="mailto:dpo@exemple.fr">dpo@exemple.fr</a>
          </li>
        </ul>
        <p>
          En cas de contestation légitime non satisfaite, vous pouvez introduire
          une réclamation auprès d'une autorité de contrôle (voir <a href="cnil.fr">cnil.fr</a>).
        </p>
      </div>

      <PartageTools />

      <footer class="os-page-date">
        <div>
          <p>
            <time class="published" datetime="2023-09-01T00:00:00+02:00">
              Publié le 01 septembre 2023
            </time>
          </p>
        </div>
      </footer>
    </main>
  </div>
</template>
<script setup>
import PartageTools from "@/components/ui/PartageTools.vue";
</script>
