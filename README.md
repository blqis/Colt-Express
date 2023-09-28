# COLT EXPRESS

Ce Colt Express est une version simplifiée qui se joue à 2 ou 3 joueurs sur un nombre fixe de wagons, ici 4. Il est donc préférable de jouer à 3 afin de respecter le ratio 1 bandit = 1 wagon + locomotive. 
Le jeu se divise en deux phases distinctes : action et planification. Par défaut, le nombre d'actions, munitions et tours est de 3 mais peut être modifié selon la durée et difficulté de jeu voulue.


## Utilisation

Ce Colt Express peut se jouer avec les 4 flèches directionnelles du clavier ainsi que les touches 'A' (action), 'S' (tirer) et 'D' (braquer). Ces mêmes commandes sont également présentes sur l'interface.


## Parties traitées

L'interface comporte plusieurs éléments : 
	- un Canvas Menu
		- Une Frame de boutons (susmentionnés),
		- un ScrolledText qui sert de compte-rendu en temps réel de la partie;
	- le Canvas Jeu où s'affichent le train ainsi que les bandits.
	
Chaque wagon, hormis la locomotive, contient un nombre aléatoire de butins entre 1 et 4, d'une valeur de 100/200 (bourse) ou 500 (bijou). Le magot présent dans la locomotive vaut 1000 et est le seul butin de ce "wagon". La position du Marshall est initialisée dans la locomotive, tandis que les bandits sont présents sur le dernier wagon (numéro 4).

Toutes les règles de ce Colt Express simplifié ont été implémentées : 
	- Le Marshall se déplace aléatoirement à l’étage inférieur pour traquer les bandits et leur fait ainsi tomber un butin au hasard (s’ils en ont) dès lors qu’ils sont dans le même wagon ;
	- Les bandits peuvent se tirer dessus (mais pas sur eux-mêmes) et perdre un butin au hasard toujours, qui se verra ajouter dans le wagon où il a été lâché ;
	- Si plus d’une cible est présente dans un même wagon, le tir sera aléatoire ;
	- L’ordre des actions est le même tout au long de la partie, et chaque bandit se voit choisir x actions l’un après l’autre ;
	- Les actions sont bien exécutées une par une et simultanément (ex : tour1 → bandit1 action1, bandit2 action1, bandit3 action1) ;


Quant à l’interface : 
- Le choix des actions, les actions en elles-mêmes ainsi qu’un récapitulatif des (ou l’absence de) butins de chaque bandit sont affichés sur le compte-rendu textuel dans une zone dédiée graphique ;
- Les boutons de commandes ont chacun une icône ;
- Les commandes clavier influent sur l’aspect visuel des boutons et produisent le même effet sonore qu’au clic ;
- Une musique se joue en boucle tout au long de la partie.


## Troubleshooting

Nous avions d’abord eu assez de mal à choisir une méthode de placement pour nos widgets au sein de nos Frames / Canvas en accord avec ce que l’on avait en tête. Nous avons finalement opté pour .grid qui a notre sens est la plus optimale pour les placements de différents widgets sur un même Canvas. Il a suffi de “jouer” avec le poids de certaines colonnes et lignes, ‘anchor’ et column/rowspan, pour avoir un bon résultat centré au millimètre près. Une fois maîtrisée, .grid a été la plus simple à utiliser pour le rendu que l’on souhaitait.

Cependant, pour le déplacement des bandits, il y a eu moins de minutie étant donné que notre image est statique. Elle n’est pas constituée d’objets wagons générés sur un fond, mais est bel et bien une image plate. Ce qui explique aussi pourquoi nous avons choisi une fenêtre non redimensionnable afin de ne pas fausser les calculs de déplacement au pixel faits sur des valeurs très spécifiques (les dimensions de notre image de fond).

Pour que les bandits puissent apparaître, nous avons également extrait les wagons sur un logiciel de digital art (Procreate), puis exporté au format .png. Nous l’avons superposé au-dessus de notre fond normal, et entre ces deux “couches” apparaissent les bandits, donnant ainsi l’illusion qu’ils sont visibles à travers les fenêtres des wagons.

Par manque d'expérience, il n’a pas été possible de dessiner les wagons. Les “assets” libres de droit ont également été difficiles à trouver vu l’angle du jeu, ce qui explique notre choix de travailler avec une image statique.

La locomotive étant considérée comme un wagon, le déplacement de (-)300 pixels sur l’axe x s’applique pour elle aussi. Mais elle est visuellement différente (une fenêtre en moins) des autres wagons et un peu plus éloignée, ce qui crée un léger décalage.

Pour optimiser le jeu, il serait préférable de générer des wagons sur un fond, et ne pas chercher des déplacements “pixel-perfect”, qui sont très vite faussés lorsque l’on veut enrichir le projet.

D’autre part, l’accord au féminin et pluriel a parfois posé souci car cela impliquait beaucoup plus de tests et conditions, “nested loops” etc. Ce problème est moins proéminent en anglais, mais nous avons décidé de rester sur du français pour ce projet.

Enfin, dans notre projet, les tirs des bandits ne se font que sur l’axe dans lequel ils se trouvent (toit/intérieur). Il n’y a pas de choix directionnels. C’est une implémentation que nous n’avons pas pu faire.

Aucun code n’a été emprunté. Tout a été réalisé en binôme à l'aide de la documentation officiel et le support de cours
