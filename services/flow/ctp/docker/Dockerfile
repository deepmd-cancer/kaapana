FROM docker.io/ubuntu:20.04 as build

LABEL IMAGE="ctp"
LABEL VERSION="0.1.3"
LABEL BUILD_IGNORE="False"

ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y --no-install-recommends \
  git \
  openjdk-8-jdk \
  ant \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /build-ctp

RUN git clone -n https://github.com/johnperry/CTP.git . && git checkout 2ae3e71ce84b425857ce0b5cca249eda2ea542ed

COPY /files/Runner.java ./source/java/org/rsna/runner/
COPY /files/PCTable.java ./source/java/org/rsna/ctp/stdstages/dicom
# added consolelogs, to directly view logs in kubernetes logs
COPY /files/log4j.properties ./source/files/

# use java 8 for correct build process
ENV JAVA_HOME /usr/lib/jvm/java-1.8.0-openjdk-amd64 
RUN ant -buildfile build.xml

COPY /files/additional-libraries ./build/CTP/libraries

COPY /files/kaapana-dag-trigger ./build/kaapana-dag-trigger

RUN cd ./build/kaapana-dag-trigger \
  && ant -buildfile build.xml

#############################################################################################
###############################           2nd STAGE           ###############################
#############################################################################################

FROM docker.io/ubuntu:20.04

RUN apt-get update && apt-get install -y --no-install-recommends \
  default-jre \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/CTP

COPY /files/config.xml ./config.xml
COPY --from=build /build-ctp/build/CTP/ ./

CMD ["java","-jar","Runner.jar"]


