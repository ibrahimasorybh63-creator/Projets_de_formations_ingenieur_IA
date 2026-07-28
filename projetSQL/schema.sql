create table clients(
    clients_id integer primary key AUTOINCREMENT,
    nom varchar(20) not null,
    prenom varchar(30) not null,
    adresse varchar(30)
);
create table produits(
    produits_id integer primary key AUTOINCREMENT,
    nom varchar(30) not null,
    prix integer not null,
    type_prod varchar(30) not null
);
create table commandes(
    commandes_id integer primary key AUTOINCREMENT,
    date_comm date ,
    clients_id integer,
    foreign key (clients_id) references clients(clients_id) ON DELETE CASCADE
);
create table details_comm (
    quantite integer not null,
    prix_unitaire integer not null,
    commandes_id integer not null,
    produits_id integer not null, 
    primary key (commandes_id,produits_id),
    foreign key (commandes_id) references commandes(commandes_id) ON DELETE CASCADE,
    foreign key (produits_id) references produits(produits_id) ON DELETE CASCADE
);