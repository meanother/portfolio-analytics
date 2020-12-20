create table if not exists operations(
    id integer not null
    , oper_date timestamap not null
    , currency varchar(50) null
    , commission real null
    , figi varchar(100) null
    , instrument_type varchar(100) null
    , is_margin_call varchar(50) null
    , operation_type varchar(255) null
    , payment real null
    , price real null
    , quantity integer null
    , quantity_executed integer null
    , status varchar(50) null
);

create table if not exists instruments(
    id integer primary key
    , currency varchar(30) not null
    , figi varchar(50) not null
    , isin varchar(50) not null
    , lot integer not null
    , min_price_increment real null
    , name varchar(255) not null
    , ticker varchar(50) not null
    , type varchar(50) null
    , min_quantity varchar(50) null
);