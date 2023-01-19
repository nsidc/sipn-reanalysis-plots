# Releasing and deploying

Releasing means making a new version of the code available.

Deploying means installing / updating the code to our infrastructure.


## Releasing

Follow these directions to release a new version of the code. *NOTE: All release tags
should be on the `main` branch!*


### CHANGELOG

Summarize the changes in the new version in the `CHANGELOG.md` under a new header `#
NEXT_VERSION` at the top of the file. Contrived example:

```
# NEXT_VERSION

- Automatically reject images with more than `MISSINGDATA_MAX_PERCENT` missing pixels.
  Defaults to `95`.
```


### Bumpversion

Increment the version using `bumpversion`. Examples:

```
bumpversion build       # bump from 3.1.0beta1 to 3.1.0beta2
bumpversion prerelease  # bump from 3.1.0alpha1 to 3.1.0beta0
bumpversion patch       # bump from 3.1.0 to 3.1.1
bumpversion minor       # bump from 3.1.0 to 3.2.0
bumpversion major       # bump from 3.1.0 to 4.0.0
```

Commit and push the change.


### Tag

Add a git tag to the latest commit. Tags must be version numbers prefixed with `v`.
Example:

```
git tag v3.2.0
```

Push the tag, being careful not to accidentally push undesired commits or tags:

```
git push origin v3.2.0
```


### Wait for automated processes

Monitor CircleCI for job completion. Monitor DockerHub for image presence. *NOTE: There is a
minor delay between completion of CircleCI and Docker image presence on DockerHub!*


## Deploy

Follow these instructions to deploy a new version of the code. You may use either of
these methods:


### Deploy with Garrison

This method is faster and enables a version-pinned deployment.

Open a Jira `PCT` ticket requesting ops to deploy a given version with Garrison, e.g.:

```
Subject: Please deploy sipn-reanalysis-plots v1.0.0 to production with Garrison

Body:

<Any special instructions>

<How to verify deployment: what to expect before/after to indicate success>
```


#### Deploy to pre-production with Garrison

You can use the [Jenkins CD server](http://ci.jenkins-cd.apps.int.nsidc.org:8080/) to
deploy to `integration` or `qa` environments. The jobs on this Jenkins server are
modeled after the operations jobs, but can only deploy to environments not managed by
the Operations team.

Simply run the `Deploy_Project_with_Garrison` job and input the correct parameters.


### Deploy with Blue/Green Swap

This method is slower and deploys whatever is on the `main` branch. *NOTE: This
deployment method _must_ be used if VM configuration (e.g. mounts, number of CPUs, or
amount of memory) is changed.*

Create a new blue machine from the `sipn-reanalysis-vm` repository:

```
vagrant nsidc up --env=blue
```

Open a `PCT` ticket requesting ops to swap the new VM to the "green" status:

```
Subject: Please blue/green swap sipn-reanalysis VM to production.

Body:

<Any special instructions>
```
