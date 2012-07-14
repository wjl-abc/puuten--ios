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
- (NSString *)replaceUnicode:(NSString *)unicodeStr {  
    
    NSString *tempStr1 = [unicodeStr stringByReplacingOccurrencesOfString:@"\\u" withString:@"\\U"];  
    NSString *tempStr2 = [tempStr1 stringByReplacingOccurrencesOfString:@"\"" withString:@"\\\""];   
    NSString *tempStr3 = [[@"\"" stringByAppendingString:tempStr2] stringByAppendingString:@"\""];  
    NSData *tempData = [tempStr3 dataUsingEncoding:NSUTF8StringEncoding];  
    NSString* returnStr = [NSPropertyListSerialization propertyListFromData:tempData  
                                                           mutabilityOption:NSPropertyListImmutable   
                                                                     format:NULL  
                                                           errorDescription:NULL];  
    
    //NSLog(@"Output = %@", returnStr);  
    
    return [returnStr stringByReplacingOccurrencesOfString:@"\\r\\n" withString:@"\n"];  
} 

@end
