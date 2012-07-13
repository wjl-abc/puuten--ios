//
//  UProfile.m
//  puuten
//
//  Created by wang jialei on 12-7-12.
//  Copyright (c) 2012年 __MyCompanyName__. All rights reserved.
//

#import "UProfile.h"

@implementation UProfile
//@synthesize name = _name;
//@synthesize lat = _lat;
@synthesize userID = _userID;

//- (id)initWithName:(NSString *)name lat:(NSString*)lat{
- (id)initWithUserID:(int)userID{
    if((self = [super init])){
        //self.name = name;
        //self.lat = lat;
        self.userID = userID;
    }
    return self;
}


@end
