FROM ali9313/lio:slim-buster

#clonning repo 
RUN git clone https://github.com/ali9313/lio.git /root/aliup
#working directory 
WORKDIR /root/aliup

# Install requirements
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs
RUN npm i -g npm
RUN pip3 install --no-cache-dir -r requirements.txt

ENV PATH="/home/aliup/bin:$PATH"

CMD ["python3","-m","aliup"]
