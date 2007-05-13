==============
AOSSI Manual
==============

:Author: Ariel De Ocampo <arieldeocampo@gmail.com>
:Version: 0.1.0
:Date: 2007-05-13

Copyright (C) 2007 Ariel De Ocampo <arieldeocampo@gmail.com>

Abstract
=========
This manual describes the purpose and usage of the aossi python utility
package. This includes a brief history of its development and its
reasons for being, a discussion on the package's development evolution,
and usage examples and recommendations.

License
=========
This work is licensed under the Creative Commons Attribution-
NonCommercial-ShareAlike 3.0 Unported License. To view a copy of this 
license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/; or, 
send a letter to Creative Commons, 543 Howard Street, 5th Floor, San 
Francisco, California, 94105, USA.

Contents
=========

- 1 Introduction

  - 1.1 What is AOSSI?

    - 1.1.1 It Can Do What?!
    - 1.1.2 A name for the unimaginative
    - 1.1.3 This feels familiar somehow...
    - 1.1.4 Aspects of Python

  - 1.2 Getting AOSSI
  - 1.3 Installing AOSSI
  - 1.4 Updating AOSSI
  - 1.2 New versions of this manual
  - 1.3 Feedback and corrections
  - 1.4 Acknowledgements
  - 1.5 Revision History

- 2 Requirements

  - 2.1 Python Versions

    - 2.1.1 Python 2.5
    - 2.1.2 Python 2.4
    - 2.1.3 Python 2.3 and older
  
  - 2.2 Required Packages

    - 2.2.1 smanstal
    - 2.2.2 anyall

- 3 Concepts

  - 3.1 Callables
  - 3.2 Signals and Slots
  - 3.3 Decorators
  - 3.4 Extensions

- 4 API Overview

  - 4.1 util

    - 4.1.1 callobj
    - 4.1.2 introspect
    - 4.1.3 odict

  - 4.2 cwrapper

    - 4.2.1 cid
    - 4.2.2 num_static_args
    - 4.2.3 CallableWrapper

  - 4.3 core

    - 4.3.1 callfunc
    - 4.3.2 Connection Helpers
      
      - 4.3.2.1 mkcallback
      - 4.3.2.2 connect_func
      - 4.3.2.3 disconnect_func
   
    - 4.3.3 BaseSignal
    - 4.3.4 getsignal

- 4 Teaching By Example

  - 4.1 The Basics

    - 4.1.1 Before and After
    - 4.1.2 Experiencing Disconnect
    - 4.1.3 Advice for the Active
    - 4.1.4 Call Me When You're Ready
    - 4.1.5 Information, Stick, Too Much Shaking?

  - 4.2 Your Very Own Signal

    - 4.2.1 Cake and Pie

      - 4.2.1.1 Around We Go
      - 4.2.1.2 Remind Me When We Return
      - 4.2.1.3 See, There's This Pipe, And...
      - 4.2.1.4 What Do You Mean "I'm Expendable"?!
      - 4.2.1.5 Choices, Choices
      - 4.2.1.6 Piece Of Cake, Easy As Pie

    - 4.2.2 Meet Me Later Than After

  - 4.3 Decorate To Renovate

    - 4.3.1 Here's Some Paint

      - 4.3.1.1 It Better Be Ready When I Get Back
      - 4.3.1.2 Fashions From Around The World
      - 4.3.1.3 On The Other Side of the Stream
      - 4.3.1.4 Make A Decision Already!
      - 4.3.1.5 Remain Flexible
      - 4.3.1.6 Let's Do It All!
      - 4.3.1.7 Is This A Black-Tie Affair?
      - 4.3.1.8 Pigs Can Fly... If They're Pink

    - 4.3.2 Standard Phone Rates Apply
    - 4.3.3 Send That Signal

