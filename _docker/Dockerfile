FROM python:3.10

RUN apt update

# Install supporting packages
RUN apt install -y vim netcat lsof
# Requirements for psycopg2 package
RUN apt install -y libpq-dev python3-dev

ENV USER appuser
ENV HOME /home/$USER

RUN pip install --upgrade pip
RUN pip install pipenv

RUN useradd -m $USER && echo $USER:$USER | chpasswd && adduser $USER sudo
ENV APP_HOME $HOME/code
RUN mkdir -p $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

# INSTALL ALL DEPENDENCIES
COPY ./Pipfile.lock $APP_HOME/Pipfile.lock
COPY ./Pipfile $APP_HOME/Pipfile

# Add .local/bin to path
ENV PATH "$PATH:$HOME/.local/bin"
RUN chown -R $USER:$USER $HOME
RUN pipenv install --system --deploy --ignore-pipfile
#
#COPY . $APP_HOME
RUN chown -R $USER:$USER $APP_HOME

USER $USER

#RUN chmod +x /home/appuser/app/docker-files/entrypoint.sh
#ENTRYPOINT ["/home/appuser/app/docker-files/entrypoint.sh"]
