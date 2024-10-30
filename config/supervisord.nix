{ pkgs, projectDir }:

let
  postgresConf = import ./postgres.nix { inherit pkgs projectDir; };
in
pkgs.writeText "supervisord.conf" ''
  [supervisord]
  logfile=data/supervisor/supervisord.log
  pidfile=data/supervisor/supervisord.pid
  strip_ansi=true

  [program:postgres]
  command=postgres -c config_file=${postgresConf} -D data/postgres
  stopsignal=INT
  stdout_logfile=data/supervisor/postgres.log
  stderr_logfile=data/supervisor/postgres.log

  [program:valkey]
  command=valkey-server config/valkey.conf
  stopsignal=INT
  stdout_logfile=data/supervisor/valkey.log
  stderr_logfile=data/supervisor/valkey.log

  [program:mailpit]
  command=mailpit -d data/mailpit/mailpit.db --enable-spamassassin spamassassin.monicz.dev:783 --smtp-auth-accept-any --smtp-auth-allow-insecure
  stopsignal=INT
  stdout_logfile=data/supervisor/mailpit.log
  stderr_logfile=data/supervisor/mailpit.log

  [program:watch-js]
  command=watch-js
  stopsignal=TERM
  stdout_logfile=data/supervisor/watch-js.log
  stderr_logfile=data/supervisor/watch-js.log

  [program:watch-locale]
  command=watch-locale
  stopsignal=TERM
  stdout_logfile=data/supervisor/watch-locale.log
  stderr_logfile=data/supervisor/watch-locale.log

  [program:watch-proto]
  command=watch-proto
  stopsignal=TERM
  stdout_logfile=data/supervisor/watch-proto.log
  stderr_logfile=data/supervisor/watch-proto.log

  [program:watch-sass]
  command=watch-sass
  stopsignal=TERM
  stdout_logfile=data/supervisor/watch-sass.log
  stderr_logfile=data/supervisor/watch-sass.log
''
